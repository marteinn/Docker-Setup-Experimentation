# 10. Docker-Composer-Ansible-Fabric 2.0

This experiment is based on experiment no 9 (ansible, compose, docker), with the purpose of arriving at a real scenario codebase.

- Refactor the django app into a strucutre where the django in fact are the main app and should be easily run in docker and local.
- Fabric dependencies should reside in its own folder.
- The django app should have some additional code so we can simulate everything from migrations to errors.
- The nginx config should be smarter and allow more sites to be plugged in.
- DB should be correctly setup, that is security wise.
- The django app should be able to run, as docker, but using runserver, toggled with a env-var.
- Vagrant should require ansible to be available before running `up`

## TODO
- Make uwsgi log to `docker logs`
- Look into making app image smaller in size
- Replace `vagrant` with deploy user for `docker-compose-prod.yml`
- Look through nginx-config



## Requirementst
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

#### Local
- Run `docker-compose up` in project-dir.
- Done! This should be enough for local development


## Vagrant
This will provision your own vagrant box running docker (based on ubuntu), with the help of ansible.

#### Installing
```
cd ansible
virtualenv venv
source venb/bin/activate
pip install -r requirements.txt
vagrant up
```
Done! You should now have a vagrant box ready for running docker.


## Deployment
Time to deploy! This project uses a deploy flow based on pulling an image from a registry using docker-compose.

#### Installing
```
cd fabric
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

When you are done installing, you can now use any of the following taks.

#### Tasks

- Perform initial setup (create folders, upload compose files and start containers)
    - `fab vagrant setup -c fabricrc.txt`

- Sync docker-compose config files
    - `fab vagrant sync_compose -c fabricrc.txt`

- Build application (django) image
    - `fab vagrant build -c fabricrc.txt`

- Push image to repro
    - `fab vagrant push -c fabricrc.txt`

- Deploy containers on remote
    - `fab vagrant deploy -c fabricrc.txt`
