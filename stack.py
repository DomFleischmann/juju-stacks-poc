""" Module in charge of Stack data structure and Files """
import os
import yaml
import component
import status


def load_stack_data(stack_name: str,) -> dict:
    """ Load the Stack Metadata file of a specific Stack """
    filename = "{}/stack.yaml".format(stack_name)
    if not os.path.isfile(filename):
        return None

    with open(filename) as file_stream:
        return yaml.safe_load(file_stream)


def load_stacks_file() -> dict:
    """ Load complete Local Stacks File """
    home = os.getenv("HOME")
    filename = "{}/.local/share/juju/stacks.yaml".format(home)

    if not os.path.isfile(filename):
        open(filename, 'w').close()

    with open(filename, "r") as s_file:
        stacks = yaml.safe_load(s_file)

    return stacks


def write_stacks_file(content: dict) -> dict:
    """ Overwrite Local Stacks File """
    home = os.getenv("HOME")

    with open("{}/.local/share/juju/stacks.yaml".format(home), "w") as s_file:
        s_file.write(yaml.dump(content))


def write_new_stack_in_file(model: str, stack_name: str, stack: dict):
    """ Write a new Stack in the local Stacks file """
    stacks = load_stacks_file()

    if stacks is None:
        stacks = {}

    if model not in stacks:
        stacks[model] = {}

    stacks[model][stack_name] = stack

    write_stacks_file(stacks)


def update_stack_in_file(model: str, stack_name: str, stack: dict):
    """ Updates an existing stack in stackfile """
    stacks = load_stacks_file()

    stacks[model][stack_name] = stack

    write_stacks_file(stacks)


def delete_stack_in_file(model: str, stack_name: str):
    """ Delete a Stack from the local Stack file """
    stacks = load_stacks_file()

    del stacks[model][stack_name]

    write_stacks_file(stacks)


def deploy_stack(stack_name: str):
    """ Deploy a Stack taken from a metadata File """
    model = status.get_current_model()
    d_stack = load_stack_data(stack_name)

    if d_stack is None:
        return False

    component.deploy_charms(d_stack["components"])
    write_new_stack_in_file(model["name"], d_stack["name"], d_stack)
    return True


def delete_stack(stackname: str) -> bool:
    """ Delete a deployed Stack """
    model = status.get_current_model()
    stacks_f = load_stacks_file()
    stacks = stacks_f[model["name"]]

    if stackname in stacks:
        component.delete_charms(stacks[stackname]["components"])
        delete_stack_in_file(model["name"], stackname)
    else:
        print("{} not found".format(stackname))
