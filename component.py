"""
Module in charge of everything related with Stack Components
"""
import subprocess


def deploy_charms(components: dict) -> bool:
    """ Deploy all the charms in the Stack """
    deploy_cmds = []
    for c_name, c_content in components.items():
        if "charm" in c_content:
            deploy_cmd = ["juju", "deploy", c_content["charm"], c_name,
                          "-n", str(c_content["num_units"])]
            config = load_config(c_content["config"])
            deploy_cmd = deploy_cmd + config
            deploy_cmds.append(deploy_cmd)

    for cmd in deploy_cmds:
        subprocess.run(cmd, check=True)


def load_config(config: dict) -> list:
    """
    Take the config of a charm and convert it into a CLI friendly format
    """
    config_list = []
    for conf_name, conf_value in config.items():
        config_list.append("--config")
        config_list.append("{}={}".format(conf_name, conf_value))

    return config_list


def delete_charms(components: dict):
    """ Delete the Charms in the Stack """
    del_cmds = []
    for c_name, c_content in components.items():
        if "charm" in c_content:
            del_cmds.append(["juju", "remove-application", c_name])

    for cmd in del_cmds:
        subprocess.run(cmd, check=True)
