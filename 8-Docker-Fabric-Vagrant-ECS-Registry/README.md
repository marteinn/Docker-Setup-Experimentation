# Docker-Fabric-Vagrant-ECS-Registry

This experiment means to explore the newly released AWS ECS Docker Registry against a docker vagrant box. The app distrubution method there will be through a registry, not as previously using load/save in docker.

## Questions
- Is it possible to work with something lika a git-hook-ish for docker, to detect updated app image and force reload?

## Requirements
- Socat on remote
- awscli on local
- Vagrant


## AWS
- Register repository
- Add AmazonEC2ContainerRegistryFullAccess to your IAM user
- Run `aws ecr get-login --region us-east-1 --profile <your_ami_user>` to obtain repro access (to obtain registry auth)
- Authenticate locally `docker login -u AWS -p ....`
- Authenticate remote `docker login -u AWS -p ....`


## Quickstart

#### Provision server
```
cd ansible
virtualenv venv
source venb/bin/activate
pip install -r requirements.txt
cd ..
vagrant up
```

#### Setup docker containers

- First add your own remote repository (based on the `django` app included)

```
cp fabricrc.example.txt fabricrc.txt
vim fabricrc.txt
```

- Create db and upload settings

```
fab vagrant setup -c fabricrc.txt
```

- Deploy app

```
fab vagrant deploy -c fabricrc.txt
```


## TODO: Release flow
- build image
- push to registry
- Make registry pull latest image
- Start new container based on new image


## References
- http://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html
- https://blog.gopheracademy.com/advent-2014/easy-deployment/
- http://www.luiselizondo.net/a-production-ready-docker-workflow/
