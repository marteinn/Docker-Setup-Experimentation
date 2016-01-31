# Docker-Fabric-Vagrant-ECS-Registry

This experiment means to explore the newly released AWS ECS Docker Registry against a docker vagrant box. The app distrubution method there will be through a registry, not as previously using load/save in docker.

All image versions are stored in the registry and we use a release tag (for instance latest) to deploy new image versions.

Having issues with image not found when running deploy for the second time? Restart the docker deamon (`service docker restart`)

This experiment currently has issues with http-timeouts when trying to restart `web`.



## Requirements
- Socat on remote
- awscli on local
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

#### Deploy tasks

- First add your own remote repository (based on the `django` app included)

```
cp fabricrc.example.txt fabricrc.txt
vim fabricrc.txt
```

- Create db and upload settings

```
fab vagrant setup -c fabricrc.txt
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

- A regular end to end deploy command would look like this.
```
fab vagrant build push deploy -c fabricrc.txt
```




## Commands

#### AWS ECR
- List repository images
`aws ecr list-images --repository-name <REPOSITORY_NAME> --region us-east-1`

- Remove remote image by tag
`aws ecr batch-delete-image --repository-name <REPOSITORY_NAME> --image-ids imageTag=<TAG_NAME> --region us-east-1`

- Remove remote image by tag
`aws ecr batch-delete-image --repository-name <REPOSITORY_NAME> --image-ids imageDigest=sha256:<IMAGE_DIGEST> --region us-east-1`


## References
- http://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html
- http://docs.aws.amazon.com/AmazonECR/latest/userguide/ECR_AWSCLI.html
- https://blog.gopheracademy.com/advent-2014/easy-deployment/
- http://www.luiselizondo.net/a-production-ready-docker-workflow/
- https://medium.com/@mccode/the-misunderstood-docker-tag-latest-af3babfd6375#.ozqrbwb0z
