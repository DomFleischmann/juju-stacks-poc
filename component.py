"""
Deploy the stack
"""
import subprocess
import stack


def deploy_charms(components: dict) -> bool:
    deploy_cmds = []
    for c_name, c_content in components.items():
        if "charm" in c_content:
            deploy_cmd = ["juju", "deploy", c_content["charm"], c_name,
                          "-n", str(c_content["num_units"])]
            config = load_config(c_content["config"])
            deploy_cmd = deploy_cmd + config
            deploy_cmds.append(deploy_cmd)

    for cmd in deploy_cmds:
        subprocess.run(cmd)



def load_config(config: dict) -> list:
    config_list = []
    for conf_name, conf_value in config.items():
        config_list.append("--config")
        config_list.append("{}={}".format(conf_name, conf_value))

    return config_list


def deploy_stack(filename: str):
    deploy_stack = stack.load_stack_file(filename)
    deploy_charms(deploy_stack["components"])
    stack.write_new_stack(deploy_stack["name"], deploy_stack)

def delete_components(components: dict):
    del_cmds = []
    for c_name, c_content in components.items():
        if "charm" in c_content:
            del_cmds.append(["juju", "remove-application", c_name])

    for cmd in del_cmds:
        subprocess.run(cmd)


def delete_stack(stackname: str):
    stacks = stack.load_stacks_file()

    if stackname in stacks:
        delete_components(stacks[stackname]["components"])
        stack.delete_stack(stackname)
