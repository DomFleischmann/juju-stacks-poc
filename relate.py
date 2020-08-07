import subprocess 
import stack


def relate_stack(provides: str, requires: str):
    p_component, p_relation = provides.split(":")
    stack_provides = get_stack_provides(p_component, p_relation)
    if stack_provides is not None:
        provides = stack_provides
    print("{}".format(provides))
    r_component, r_relation = requires.split(":")
    stack_requires = get_stack_requires(r_component, r_relation)
    if stack_requires is not None:
        requires = stack_requires
    print("{}".format(requires))
    subprocess.run(["juju", "add-relation", provides, requires])


def get_stack_provides(comp: str, rel: str) -> str:
    stacks = stack.load_stacks_file()
    if stacks is None:
        return
    if comp not in stacks:
        return

    p_stack = stacks[comp]

    return p_stack["provides"][rel]["forward"]


def get_stack_requires(comp: str, rel: str) -> str:
    stacks = stack.load_stacks_file()
    if stacks is None:
        return
    if comp not in stacks:
        return

    p_stack = stacks[comp]

    return p_stack["requires"][rel]["forward"]
