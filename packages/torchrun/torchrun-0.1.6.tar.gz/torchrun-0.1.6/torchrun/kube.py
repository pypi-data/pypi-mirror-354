import os
import sys
import time
import yaml
import subprocess
from .compat import get_rocm_image_for_torch_version


def get_torch_version_from_requirements(path: str) -> str:
    print(f"[torchrun] Reading torch version from {path}")
    with open(path) as f:
        for line in f:
            if line.startswith("torch"):
                parts = line.strip().split("==")
                if len(parts) == 2:
                    print(f"[torchrun] Found torch version: {parts[1]}")
                    return parts[1]
                else:
                    print("[torchrun] No version specified, using default: 2.2.2")
                    return "2.2.2"
    raise ValueError("[torchrun] torch version not found in requirements.txt")


def deploy_pod_for_requirements(requirements_path: str):
    print(f"[torchrun] Deploying pod for requirements: {requirements_path}")

    try:
        torch_version = get_torch_version_from_requirements(requirements_path)
    except Exception as e:
        print(f"[torchrun][error] Failed to get torch version: {e}")
        sys.exit(1)

    image = get_rocm_image_for_torch_version(torch_version)
    pod_name = f"torchrun-{torch_version.replace('.', '-')}-pod"
    yaml_path = "torchrun_pod.yaml"

    pod_spec = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "name": pod_name,
            "namespace": "default"
        },
        "spec": {
            "volumes": [
                {"name": "kfd", "hostPath": {"path": "/dev/kfd", "type": "CharDevice"}},
                {"name": "dri", "hostPath": {"path": "/dev/dri", "type": "Directory"}},
                {"name": "workspace", "emptyDir": {}},
                {"name": "scratch", "emptyDir": {}}
            ],
            "initContainers": [
                {
                    "name": "init-copy",
                    "image": "python:3.10",
                    "command": ["/bin/sh", "-c", "cp -r /source/* /workspace/ || true"],
                    "volumeMounts": [
                        {"name": "workspace", "mountPath": "/workspace"},
                        {"name": "scratch", "mountPath": "/source"}
                    ]
                }
            ],
            "containers": [
                {
                    "name": "torch-container",
                    "image": image,
                    "command": ["/bin/bash", "-c", "pip install -r /workspace/requirements.txt && exec bash"],
                    "stdin": True,
                    "tty": True,
                    "volumeMounts": [
                        {"name": "kfd", "mountPath": "/dev/kfd"},
                        {"name": "dri", "mountPath": "/dev/dri"},
                        {"name": "workspace", "mountPath": "/workspace"}
                    ],
                    "securityContext": {
                        "privileged": True,
                        "runAsUser": 0,
                        "runAsGroup": 0,
                        "capabilities": {"add": ["SYS_PTRACE"]}
                    }
                }
            ],
            "restartPolicy": "Always",
            "hostNetwork": True,
            "hostIPC": True,
            "imagePullSecrets": [
                {"name": "gcp-docker-virtual"},
                {"name": "gcr-json-key"}
            ],
            "tolerations": [
                {
                    "key": "node.kubernetes.io/not-ready",
                    "operator": "Exists",
                    "effect": "NoExecute",
                    "tolerationSeconds": 300
                },
                {
                    "key": "node.kubernetes.io/unreachable",
                    "operator": "Exists",
                    "effect": "NoExecute",
                    "tolerationSeconds": 300
                }
            ]
        }
    }

    print(f"[torchrun] Writing pod spec to {yaml_path}")
    with open(yaml_path, "w") as f:
        yaml.safe_dump(pod_spec, f)

    print(f"[torchrun] Deleting existing pod (if any): {pod_name}")
    subprocess.run(["kubectl", "delete", "pod", pod_name], capture_output=True)

    print(f"[torchrun] Applying pod spec with kubectl...")
    try:
        result = subprocess.run(["kubectl", "apply", "-f", yaml_path], capture_output=True, text=True, check=True)
        print(f"[torchrun][kubectl apply] stdout:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"[torchrun][error] Failed to apply pod spec:\n{e.stderr}")
        sys.exit(e.returncode)

    print(f"[torchrun] Waiting for pod to reach Running state...")
    while True:
        result = subprocess.run(
            ["kubectl", "get", "pod", pod_name, "-o", "jsonpath={.status.phase}"],
            capture_output=True, text=True
        )
        phase = result.stdout.strip()
        if phase == "Running":
            break
        elif "Error" in phase or "Failed" in phase:
            print(f"[torchrun][error] Pod entered failure state: {phase}")
            sys.exit(1)
        time.sleep(1)

    print(f"[torchrun] Copying local directory into /source ...")
    try:
        result = subprocess.run(["kubectl", "cp", ".", f"{pod_name}:/source"], capture_output=True, text=True, check=True)
        print(f"[torchrun][kubectl cp] stdout:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"[torchrun][error] Failed to copy files into pod:\n{e.stderr}")
        sys.exit(e.returncode)

    print(f"[torchrun] Pod {pod_name} is ready. Attach with: kubectl exec -it {pod_name} -- bash")