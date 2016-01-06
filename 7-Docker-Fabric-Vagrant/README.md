# Docker-Fabric-Vagrant
The purpose of this experiment is to use fabric as a container orchestation tool (either with regular fabric or with docker-fabric). Ansible is used for the initial server preparation.


## Requirements
- Socat (`brew install socat`)


## Quickstart

### Provision server
```
cd ansible
virtualenv venv
source venb/bin/activate
vagrant up
```

### Execute fabric commands
(Make sure you are not running in the ansible virtualenv from previous step)

```
virtualenv venv
source venv/bin/activate
fab vagrant uname -c fabricrc.txt
```


## Commands
### Vagrant
- vagrant ssh-config

### Fabric
- fab docker.version


## References
- https://www.amon.cx/blog/deploying-web-apps-docker/
