"""
Module in charge of representing the status
"""
import subprocess
import yaml


def get_current_model() -> dict:
    """ Get the currently used model which its information """
    status = get_juju_status()
    return status["model"]


def get_juju_status() -> dict:
    """ Get juju status converted into a dictionary """
    cmd = ["juju", "status", "--format", "yaml"]
    result = subprocess.run(cmd, capture_output=True, check=True)
    return yaml.safe_load(result.stdout)


def juju_status_with_stack() -> str:
    """ Extend juju status with stack information """
    cmd = ["juju", "status"]

    result = subprocess.run(cmd, capture_output=True, check=True)

    return result.stdout.decode("utf-8").replace("-s-", ".")
