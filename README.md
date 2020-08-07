# Juju Stacks PoC

This is a samll PoC of the Juju Stacks concept.


## How to Use

You can check all the options available with:

`./juju-stack --help`

When a stack is deployed its information will be stored in `~/.local/share/juju/stacks.yaml`
### Deploy a Stack
`./juju-stack --deploy test-stacks/mysql-stack.yaml`

### List all Stacks
`./juju-stack --list`

### Show a stack
`./juju-stack --show mydatabase-stack`

### Delete a Stack
`./juju-stack --delete mydatabase-stack`

### Relate a Stack with another component
`./juju-stack --relate mydatabase-stack:mydatabase-db wordpress:db`
