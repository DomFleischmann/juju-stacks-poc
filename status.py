"""
Module in charge of representing the status
"""
import subprocess
import yaml
import stack


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

    new_status = result.stdout.decode("utf-8")

    new_status += "Stack \n"
    stacks = stack.get_stacks_from_current_model()

    for single_stack in stacks:
        new_status += "{} \n".format(single_stack)

    return new_status


def juju_status_with_stack_expanded() -> str:
    """ Extend juju status with stack information """
    cmd = ["juju", "status"]

    result = subprocess.run(cmd, capture_output=True, check=True)

    new_status = result.stdout.decode("utf-8")

    new_status += "Stack \n"
    stacks = stack.get_stacks_from_current_model()

    for s_key, s_value in stacks.items():
        new_status += "{} \n".format(s_key)
        for comp_key, comp_val in s_value["components"].items():
            if "charm" in comp_val:
                new_status += "    {}   application".format(comp_key)

    return new_status
