#!/usr/bin/env python3
"""
Module for the Juju Stack CLI
"""
import argparse
import subprocess
import stack
import relate
import status


def execute_juju_cmd(cmd: list):
    """ Passthrough Arguments to Juju CLI """
    cmd = ["juju"] + cmd

    result = subprocess.run(cmd, capture_output=True, check=True)

    print(result.stdout.decode("utf-8").replace("-s-", "."))


def adapt_naming(cmd: list) -> list:
    """ Change application naming """
    stacks = stack.get_stacks_from_current_model()

    for s_stack in stacks:
        for i in range(len(cmd)):
            if s_stack in cmd[i]:
                cmd[i] = cmd[i].replace(".", "-s-")
    return cmd


PARSER = argparse.ArgumentParser(description="Juju Stack CLI")
PARSER.add_argument("cmd", nargs="*", help="Juju command")

ARGS, UNKNOWN = PARSER.parse_known_args()

stack.update_stacks_from_status()

if ARGS.cmd:
    CMD = adapt_naming(ARGS.cmd + UNKNOWN)
    if CMD[0] == "deploy":
        if not stack.deploy_stack(CMD[1]):
            execute_juju_cmd(CMD)
    elif CMD[0] == "relate" or CMD[0] == "add-relation":
        relate.relate_stack(CMD[1], CMD[2])
    elif CMD[0] == "remove-stack":
        stack.delete_stack(CMD[1])
    elif CMD[0] == "config":
        execute_juju_cmd(CMD)
        if len(CMD) > 2:
            stack.update_stack_config(CMD)
    elif CMD[0] == "update-stack":
        stack.update_stacks_from_status()
    else:
        execute_juju_cmd(CMD)
