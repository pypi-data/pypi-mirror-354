import yaml
import subprocess
from .compat import get_rocm_image_for_torch_version


def get_torch_version_from_requirements(path: str) -> str:
    with open(path) as f:
        for line in f:
            if line.startswith("torch"):
                parts = line.strip().split("==")
                if len(parts) == 2:
                    return parts[1]
    raise ValueError("torch version not found in requirements.txt")


def deploy_pod_for_requirements(requirements_path: str):
    torch_version = get_torch_version_from_requirements(requirements_path)
    image = get_rocm_image_for_torch_version(torch_version)
    pod_spec = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {"name": f"torchrun-{torch_version.replace('.', '-')}-pod"},
        "spec": {
            "containers": [
                {
                    "name": "torch",
                    "image": image,
                    "command": ["sleep", "infinity"]
                }
            ],
            "restartPolicy": "Never"
        }
    }
    with open("torchrun_pod.yaml", "w") as f:
        yaml.safe_dump(pod_spec, f)
    subprocess.run(["kubectl", "apply", "-f", "torchrun_pod.yaml"])
