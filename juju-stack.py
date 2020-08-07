#!/usr/bin/env python3

import argparse
import component
import relate
import stack


parser = argparse.ArgumentParser(description="Juju Stack CLI")
parser.add_argument("--list", action="store_true", help="List all the stacks")
parser.add_argument("--show", action="store", help="Show a Stack")
parser.add_argument("--deploy", action="store", help="Deploy a Stack")
parser.add_argument("--delete", action="store", help="Delete a Stack")
parser.add_argument("--update", nargs="*", help="Update a Stack")
parser.add_argument("--relate", nargs=2,
                    help="Relate a Stack Endpoint")

args = parser.parse_args()

if args.deploy:
    component.deploy_stack(args.deploy)

if args.relate:
    print(args.relate)
    relate.relate_stack(args.relate[0], args.relate[1])

if args.delete:
    component.delete_stack(args.delete)

if args.list:
    stack_list = stack.list_stacks()
    for stack_item in stack_list:
        print(stack_item)

if args.show:
    my_stack = stack.show_stack(args.show)
    print(my_stack)
