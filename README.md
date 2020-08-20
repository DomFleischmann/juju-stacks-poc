# Juju Stacks Prototype

This is a samll Prototype of the Juju Stacks concept.


## How to Use

Using `./juju-stack` should be identical to the juju cli just changing the executable.

When a stack is deployed its information will be stored in `~/.local/share/juju/stacks.yaml`

### Deploy a Stack
`./juju-stack deploy test-stacks/mysql-stack`

### Delete a Stack
`./juju-stack remove-stack mysql`

### Relate a Stack with another component
`./juju-stack relate mysql:db wordpress:db`
`./juju-stack add-relation mysql:db wordpress:db`

### Stack Status
`./juju-stack status`
