# Juju Stacks Prototype

This is a samll Prototype of the Juju Stacks concept.


## How to Use

Using `./juju-stack` should be identical to the juju cli just changing the executable.

When a stack is deployed its information will be stored in `~/.local/share/juju/stacks.yaml`

### Deploy a Stack
`./juju-stack deploy test-stacks/mysql-stack`

### Delete a Stack
`./juju-stack remove-stack mydatabase-stack`

### Relate a Stack with another component
`./juju-stack relate mydatabase-stack:mydatabase-db wordpress:db`
`./juju-stack add-relation mydatabase-stack:mydatabase-db wordpress:db`

### Stack Status
`./juju-stack status`

More detail:
`./juju-stack status --expand-stacks`
