import subprocess
import requests
from requests.auth import HTTPBasicAuth
import yaml
from griddot.tools.utils import get_container_command


def helm_list_charts():
    encoded_project = requests.utils.quote("griddot/packages", safe="")
    url = f"https://gitlab.com/api/v4/projects/{encoded_project}/packages/helm/stable/index.yaml"

    # GitLab expects: username = anything (often 'gitlab-ci-token'), password = the token
    auth = HTTPBasicAuth("helm-user", "glpat-mKckaB2sg2vC74xzFWWB")  # or "gitlab-ci-token", token

    response = requests.get(url, auth=auth)
    response.raise_for_status()

    index = yaml.safe_load(response.text)
    return list(index.get("entries", {}).keys())


def helm_template(deployment: str, values_path: str = None):
    """
    Create a Kubernetes deployment using helm, from the possible deployments in list_helm_charts.
    """
    container_cmd = get_container_command()
    if values_path:
        values_option = f"-f {values_path}"
        values_mount = f"-v {values_path}:/values.yaml"
    else:
        values_option = ""
        values_mount = ""

    result = subprocess.run(
        f"{container_cmd} run --rm {values_mount} registry.gitlab.com/griddot/packages/helm:latest helm template griddot/{deployment} {values_option}",
        shell=True, check=True, capture_output=True
    )

    return result.stdout.decode('utf-8')
