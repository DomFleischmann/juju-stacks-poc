""" Module in charge of Stack data structure and Files """
import os
import yaml
import component


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
    with open("{}/.local/share/juju/stacks.yaml".format(home), "r") as s_file:
        stacks = yaml.safe_load(s_file)

    return stacks


def write_stacks_file(content: dict) -> dict:
    """ Overwrite Local Stacks File """
    home = os.getenv("HOME")

    with open("{}/.local/share/juju/stacks.yaml".format(home), "w") as s_file:
        s_file.write(yaml.dump(content))


def write_new_stack_in_file(stack_name: str, stack: dict):
    """ Write a new Stack in the local Stacks file """
    stacks = load_stacks_file()

    stacks[stack_name] = stack

    write_stacks_file(stacks)


def delete_stack_in_file(stack_name: str):
    """ Delete a Stack from the local Stack file """
    stacks = load_stacks_file()

    del stacks[stack_name]

    write_stacks_file(stacks)


def list_stacks() -> list:
    """ List all the deployed Stacks """
    return load_stacks_file().keys()


def show_stack(stack_name: str) -> str:
    """ Show a specific Stack """
    stacks = load_stacks_file()

    if stack_name in stacks:
        return yaml.dump(stacks[stack_name])


def deploy_stack(stack_name: str):
    """ Deploy a Stack taken from a metadata File """
    d_stack = load_stack_data(stack_name)

    if d_stack is None:
        return False

    component.deploy_charms(d_stack["components"])
    write_new_stack_in_file(d_stack["name"], d_stack)
    return True


def delete_stack(stackname: str) -> bool:
    """ Delete a deployed Stack """
    stacks = load_stacks_file()

    if stackname in stacks:
        component.delete_charms(stacks[stackname]["components"])
        delete_stack_in_file(stackname)
