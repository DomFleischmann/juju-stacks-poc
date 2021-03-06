""" Module in charge of Relating a Stack with another component """
import subprocess
import stack


# This code is ugly and could improve a lot.
def relate_stack(provides: str, requires: str):
    """ Execute Relation with Stack Relations if they exist """
    p_component, p_relation = provides.split(":")
    stack_provides = get_stack_provides(p_component, p_relation)
    if stack_provides is not None:
        provides = stack_provides

    r_component, r_relation = requires.split(":")
    stack_requires = get_stack_requires(r_component, r_relation)
    if stack_requires is not None:
        requires = stack_requires

    subprocess.run(["juju", "add-relation", provides, requires], check=True)


def get_stack_provides(s_stack: str, relation: str) -> str:
    """ Checks if Component has Provides Relation """
    stacks = stack.get_stacks_from_current_model()

    if stacks is None:
        return None

    if s_stack not in stacks:
        return None

    forward = stacks[s_stack]["provides"][relation]["forward"]

    return "{}-s-{}".format(stacks[s_stack]["name"], forward)


def get_stack_requires(component: str, relation: str) -> str:
    """ Checks if Component has Requires Relation """
    stacks = stack.get_stacks_from_current_model()

    if stacks is None:
        return None
    if component not in stacks:
        return None

    p_stack = stacks[component]

    return p_stack["requires"][relation]["forward"]
