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
    stacks = get_stacks_from_current_model()

    for single_stack in stacks:
        new_status += "{} \n".format(single_stack)

    return new_status


def juju_status_with_stack_expanded() -> str:
    """ Extend juju status with stack information """
    cmd = ["juju", "status"]

    result = subprocess.run(cmd, capture_output=True, check=True)

    new_status = result.stdout.decode("utf-8")

    new_status += "Stack \n"
    stacks = get_stacks_from_current_model()

    for s_key, s_value in stacks.items():
        new_status += "{} \n".format(s_key)
        for comp_key, comp_val in s_value["components"].items():
            if "charm" in comp_val:
                new_status += "    {}   application".format(comp_key)

    return new_status


def get_stacks_from_current_model() -> dict:
    """ Get all the stacks that are available in current model """
    model = get_current_model()
    stacks_f = stack.load_stacks_file()
    return stacks_f[model["name"]]


def update_stacks_from_status():
    """ Check Status if stack has changed and update it """
    status = get_juju_status()
    model = get_current_model()

    stacks = get_stacks_from_current_model()

    for s_key, s_value in stacks.items():
        comps = s_value["components"]
        apps = status["applications"]

        common_components = list(set(comps.keys()) &
                                 set(apps.keys()))

        for comp in common_components:
            if len(apps[comp]["units"]) != comps[comp]["num_units"]:
                new_value = s_value.copy()
                new_value["components"][comp]["num_units"] = len(apps[comp]["units"]) 
                stack.update_stack_in_file(model["name"], s_key, new_value)
