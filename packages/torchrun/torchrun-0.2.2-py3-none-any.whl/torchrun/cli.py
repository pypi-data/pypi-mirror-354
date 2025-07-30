import typer
from .kube import deploy_pod_for_requirements

app = typer.Typer()

@app.command()
def deploy(requirements: str = "requirements.txt"):
    """Deploy a ROCm-compatible pod based on requirements.txt"""
    deploy_pod_for_requirements(requirements)

if __name__ == "__main__":
    app()