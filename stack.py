import os
import yaml


def load_stack_file(filename: str,) -> dict:
    """ Load the stack yaml and convert it into a dict """
    with open(filename) as file_stream:
        return yaml.safe_load(file_stream)


def write_new_stack(stack_name: str, stack: dict):
    home = os.getenv("HOME")

    with open("{}/.local/share/juju/stacks.yaml".format(home), "r") as f:
        stacks = yaml.safe_load(f)
        if stacks is None:
            stacks = {}
        stacks[stack_name] = stack

    with open("{}/.local/share/juju/stacks.yaml".format(home), "w") as f:
        f.write(yaml.dump(stacks))


def delete_stack(stack_name: str):
    home = os.getenv("HOME")

    with open("{}/.local/share/juju/stacks.yaml".format(home), "r") as f:
        stacks = yaml.safe_load(f)
        if stack_name in stacks:
            del stacks[stack_name]

    with open("{}/.local/share/juju/stacks.yaml".format(home), "w") as f:
        f.write(yaml.dump(stacks))


def load_stacks_file() -> dict:
    home = os.getenv("HOME")
    with open("{}/.local/share/juju/stacks.yaml".format(home), "r") as f:
        stacks = yaml.safe_load(f)

    return stacks

def list_stacks() -> list:
    home = os.getenv("HOME")
    with open("{}/.local/share/juju/stacks.yaml".format(home), "r") as f:
        stacks = yaml.safe_load(f)
    
    return stacks.keys()


def show_stack(stack_name: str) -> str:
    home = os.getenv("HOME")
    with open("{}/.local/share/juju/stacks.yaml".format(home), "r") as f:
        stacks = yaml.safe_load(f)
    
    if stack_name in stacks:
        return yaml.dump(stacks[stack_name])

