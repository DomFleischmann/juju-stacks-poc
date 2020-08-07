#!/usr/bin/env python3
"""
Module for the Juju Stack CLI
"""


import argparse
import relate
import stack


PARSER = argparse.ArgumentParser(description="Juju Stack CLI")
PARSER.add_argument("--list", action="store_true", help="List all the stacks")
PARSER.add_argument("--show", action="store", help="Show a Stack")
PARSER.add_argument("--deploy", action="store", help="Deploy a Stack")
PARSER.add_argument("--delete", action="store", help="Delete a Stack")
PARSER.add_argument("--update", nargs="*", help="Update a Stack")
PARSER.add_argument("--relate", nargs=2,
                    help="Relate a Stack Endpoint")

ARGS = PARSER.parse_args()

if ARGS.deploy:
    stack.deploy_stack(ARGS.deploy)

if ARGS.relate:
    print(ARGS.relate)
    relate.relate_stack(ARGS.relate[0], ARGS.relate[1])

if ARGS.delete:
    stack.delete_stack(ARGS.delete)

if ARGS.list:
    for stack_item in stack.list_stacks():
        print(stack_item)

if ARGS.show:
    print(stack.show_stack(ARGS.show))
