"""
A docker release flow that uses load/saVe rather then repository for dealin
with app releases.

This fabric flow uses two taks, setup and deploy.

setup
    Pull postgres and nginx images
    Setup and run postgres container
    Upload nginx config to /home/vagrant/...

deploy
    Retrive new release name
    Build new app image (django) with the new release name
    Save image as tar
    Upload tar to remote
    Load image from tar to docker on remote
    Stop and remove previous app container (web)
    Remove previous app image tagged as latest
    Clean up older releases (only keep 3 + latest)
    Remove tars
    Reconstruct nginx container
"""

import os

from fabric.api import env, local, run, warn_only
from fabric.decorators import task
from fabric.operations import put

from dockerfabric.apiclient import docker_fabric


# Hard coded config vars
ssh_key_path = os.path.join(os.getcwd(), ".vagrant", "machines", "default",
                            "virtualbox", "private_key")
image_dir = "django"
image_repository = "marteinn/fabric-example-django"


@task
def vagrant():

    env.user = 'vagrant'
    env.hosts = ['127.0.0.1:2222']
    env.key_filename = ssh_key_path

    env.docker_tunnel_local_port = 22025
    env.timeout = 30


@task
def test():
    run('uname -a')


@task
def setup():
    """
    Pull needed official images, setup db and add nginx settings
    """

    docker_fabric().pull("postgres:latest")
    docker_fabric().create_container("postgres", name="db",
                                     ports=["5432"])

    # TODO: Add restart policy
    docker_fabric().start("db",
                          restart_policy={
                              'MaximumRetryCount': 0,
                              'Name': 'always'
                          },
                          binds={
                              '/home/var/lib/postgresql/data': {
                                  'bind': '/var/lib/postgresql/data',
                                  'rw': True
                              }
                          })

    # Create nginx path
    run("mkdir -p /home/vagrant/var/nginx/conf")
    docker_fabric().pull("nginx:latest")

    # Upload nginx config
    config_path = os.path.join(os.getcwd(), "files", "nginx.conf")
    put(config_path, "/home/vagrant/var/nginx/conf/nginx.conf")


@task
def deploy():
    """
    Run deployment process
    """
    # Retrive app version from app image dockerfile
    deploy_version = local('cat %s/Dockerfile | \
                           grep -e "^LABEL.version" | \
                           cut -d \\" -f 2' %
                           image_dir, capture=True)

    # Build docker app image
    local("docker build -t %s:%s %s" % (image_repository, deploy_version,
                                        image_dir))

    # Save docker app image
    local("docker save %s:%s > /tmp/docker_image.tar" % (image_repository,
                                                         deploy_version))

    # Copy docker app image to machine
    put("/tmp/docker_image.tar", "/tmp/docker_image.tar")

    # Load docker image
    run("docker load < /tmp/docker_image.tar")

    # Stop nginx before removing web
    try:
        docker_fabric().stop("nginx")
    except Exception as e:
        print("Nginx has not been created yet.")
        print(e)
        pass

    # Remove old running app container
    try:
        docker_fabric().stop("web")
    except Exception as e:
        print("Container Web has not been started")
        print(e)
        pass

    try:
        docker_fabric().remove_container("web")
    except Exception as e:
        print("Container web cannot be removed")
        print(e)
        pass

    # Remove previous app docker image
    try:
        docker_fabric().remove_image("%s:latest" % image_repository)
    except:
        print("Image not found")
        pass

    # Duplicate deploy app image and tag it latest
    run("docker tag %s:%s %s:latest" % (image_repository, deploy_version,
                                        image_repository))

    # Remove older releases of app image
    with warn_only():
        run('docker images | \
            grep %s | \
            grep -v latest | \
            awk \'{print "%s:"$2}\' | \
            tail -n +4 | \
            xargs -n 1 docker rmi' % (image_repository, image_repository))

    # Remove local app image export
    local("rm /tmp/docker_image.tar")

    # Remove remote app image export
    run("rm /tmp/docker_image.tar")

    # Start app container
    docker_fabric().create_container("%s:%s" % (image_repository, "latest"),
                                     name="web", ports=["8080"])

    docker_fabric().start("web", links={
        "db": "db"
    })

    reload_nginx()


@task
def reload_nginx():
    # Remove old running nginx container
    try:
        docker_fabric().stop("nginx")
        docker_fabric().remove_container("nginx")
    except:
        print("Nginx has not been started")
        pass

    # Setup and run nginx container
    docker_fabric().create_container("nginx:latest", name="nginx",
                                     ports=["80:80"])
    docker_fabric().start("nginx",
                          port_bindings={80: 80},
                          restart_policy={
                              'MaximumRetryCount': 0,
                              'Name': 'always'
                          },
                          binds={
                              '/home/vagrant/var/nginx/conf': {
                                  'bind': '/etc/nginx',
                                  'ro': True
                              }
                          },
                          links={
                              "web": "web"
                          })
