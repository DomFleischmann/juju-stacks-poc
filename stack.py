""" Module in charge of Stack data structure and Files """
import component
import status
import files
import relate


def deploy_stack(stack_name: str):
    """ Deploy a Stack taken from a metadata File """
    model = status.get_current_model()
    d_stack = files.load_stack_data(stack_name)

    if d_stack is None:
        return False

    component.deploy_charms(d_stack["name"], d_stack["components"])
    files.write_new_stack_in_file(model["name"], d_stack["name"], d_stack)
    if "relations" in d_stack:
        for rel in d_stack["relations"]:
            provider = "{}-s-{}".format(d_stack["name"], rel["provider"])
            requirer = "{}-s-{}".format(d_stack["name"], rel["requirer"])
            relate.relate_stack(provider, requirer)

    return True


def delete_stack(stackname: str) -> bool:
    """ Delete a deployed Stack """
    model = status.get_current_model()
    stacks_f = files.load_stacks_file()
    stacks = stacks_f[model["name"]]

    if stackname in stacks:
        component.delete_charms(stackname, stacks[stackname]["components"])
        files.delete_stack_in_file(model["name"], stackname)
    else:
        print("{} not found".format(stackname))


def get_stacks_from_current_model() -> dict:
    """ Get all the stacks that are available in current model """
    model = status.get_current_model()
    stacks_f = files.load_stacks_file()
    if model["name"] not in stacks_f:
        stacks_f[model["name"]] = {}
    return stacks_f[model["name"]]


def update_stacks_from_status():
    """ Check Status if stack has changed and update it """
    juju_status = status.get_juju_status()
    model = status.get_current_model()

    stacks = get_stacks_from_current_model()

    for s_key, s_value in stacks.items():
        comps = s_value["components"]
        apps = juju_status["applications"]

        common_components = list(set(comps.keys()) &
                                 set(apps.keys()))

        for comp in common_components:
            status_units = len(apps[comp]["units"])
            if status_units != comps[comp]["num_units"]:
                new_value = s_value.copy()
                new_value["components"][comp]["num_units"] = status_units
                files.update_stack_in_file(model["name"], s_key, new_value)


def update_stack_config(cmd: list):
    """
    Check if config command affected any stack component and update the stack
    """
    stacks = get_stacks_from_current_model()
    model = status.get_current_model()

    comp = cmd[1]
    for s_key, s_value in stacks.items():
        if comp in s_value["components"]:
            comp_dict = s_value["components"][comp]
            new_config = component.update_configs(comp_dict, cmd[2:])
            new_value = s_value.copy()
            new_value["components"][comp]["config"] = new_config
            files.update_stack_in_file(model["name"], s_key, new_value)
