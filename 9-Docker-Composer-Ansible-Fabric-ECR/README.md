# 9. Docker-Composer-Ansible-Fabric

The purpose of this experiment is to construct a deploy flow around docker-compose together with fabric.

- We'll orchestate using ansible and vagrant, like previous experiments.
- Setup and handle containers with docker-compose
- Use fabric to push and handle images and trigger container restarts
- Lets begin!


## Requirements
- awscli on local and remote
- Vagrant
- Ansible


## AWS
- Register repository
- Add AmazonEC2ContainerRegistryFullAccess to your IAM user (not in prod please)
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


## Fabric
- Perform initial setup (create folders, upload compose files and start containers)

```
fab vagrant setup -c fabricrc.txt
```

- Sync compose config files

```
fab vagrant sync_compose -c fabricrc.txt
```

- Build application (django) image

```
fab vagrant build -c fabricrc.txt
```

- Push image to repro

```
fab vagrant push -c fabricrc.txt
```

- Deploy containers on remote

```
fab vagrant deploy -c fabricrc.txt
```


## TODO:
- (Done!) Add .env file to web-container
- (Done!) Add `pip install aws..` script in ansible
- (Done!) Add code to handle aws ECR re-auth when token expires
    - (Done!) Local
    - (Done!) Remote
