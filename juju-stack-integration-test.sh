#! /usr/bin/env bash
juju destroy-model test
juju add-model test
juju deploy wordpress
sleep 60
./juju-stack --deploy test-stacks/mysql-stack.yaml
sleep 60
./juju-stack --list
./juju-stack --show mydatabase-stack
./juju-stack --relate mydatabase-stack:mydatabase-db wordpress:db
./juju-stack --delete mydatabase-stack
