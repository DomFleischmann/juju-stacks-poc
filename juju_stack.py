#!/usr/bin/env python3
"""
Module for the Juju Stack CLI
"""
import argparse
import subprocess
import stack
import relate


def execute_juju_cmd(cmd: str):
    """ Passthrough Arguments to Juju CLI """
    cmd = ["juju"] + cmd
    subprocess.run(cmd, check=True)


PARSER = argparse.ArgumentParser(description="Juju Stack CLI")
PARSER.add_argument("cmd", nargs="*", help="Juju command")

ARGS, UNKNOWN = PARSER.parse_known_args()

if ARGS.cmd:
    CMD = ARGS.cmd + UNKNOWN
    if CMD[0] == "deploy":
        if not stack.deploy_stack(CMD[1]):
            execute_juju_cmd(CMD)
    elif CMD[0] == "relate" or CMD[0] == "add-relation":
        relate.relate_stack(CMD[1], CMD[2])
    elif CMD[0] == "remove-stack":
        stack.delete_stack(CMD[1])
    else:
        execute_juju_cmd(CMD)
