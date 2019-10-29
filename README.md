# My home assistant config

## Deploying config with ansible
### Setup
There are various variables that `deploy_config.yml` depends on. These need to be added to the inventory unless they have a default value.

#### Env variables
Set these to configure ansible

The ansible inventory path. `ANSIBLE_INVENTORY`  
The ansible vault password file: `ANSIBLE_VAULT_PASSWORD_FILE`

### Inventory
`deploy_config.yml` is configured to execute on hosts that are in the `home_assistant` group.

## Remote user
The playbook is configured to run as root. This can be changed with setting the ansible variable `hass_remote_user`


## Deploy
Might be good to run with diff and check to make sure it all looks good
```
ansible-playbook deploy_config.yml --diff --check
```
Remove `--check` to apply the changes