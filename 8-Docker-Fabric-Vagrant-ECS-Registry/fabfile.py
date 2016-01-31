"""
A docker release flow that delivers the app image using amazons docker registry

This fabric flow uses two taks, setup and deploy.
setup
    Pull postgres and nginx images
    Setup and run postgres container
    Upload nginx config to /home/vagrant/...
build
    Build new app image (django) with the new release name
push
    Remove old image with release tag from registry
    Upload new release image
deploy
    Pull latest image from registry
    Reconstruct nginx container
    Restart web container
"""

import os

from fabric.api import env, local, run
from fabric.decorators import task
from fabric.operations import put

from dockerfabric.apiclient import container_fabric
from dockerfabric import yaml


# Hard coded config vars
ssh_key_path = os.path.join(os.getcwd(), ".vagrant", "machines", "default",
                            "virtualbox", "private_key")
ssh_user = 'vagrant'
web_dir = "django"

# Create docker map
docker_map_path = os.path.join(os.getcwd(), "docker_map.yaml")
docker_maps = yaml.load_map_file(docker_map_path, 'docker_map')
env.docker_maps = docker_maps


@task
def vagrant():
    env.user = 'vagrant'
    env.hosts = ['127.0.0.1:2222']
    env.key_filename = ssh_key_path

    env.docker_tunnel_local_port = 22025
    env.timeout = 60


@task
def test():
    run('uname -a')


@task
def setup():
    # Create postgresql data path
    run("mkdir -p /home/%s/var/lib/postgresql/data" % ssh_user)

    # Create postgres db
    container_fabric().startup('db')

    # Create nginx path
    run("mkdir -p /home/%s/var/nginx/conf" % ssh_user)

    # Upload nginx config
    config_path = os.path.join(os.getcwd(), "files", "nginx.conf")
    put(config_path, "/home/%s/var/nginx/conf/nginx.conf" % ssh_user)


def _read_tag():
    # Retrive app version from app image dockerfile
    deploy_version = local('cat %s/Dockerfile | \
                           grep -e "^LABEL.version" | \
                           cut -d \\" -f 2' %
                           web_dir, capture=True)

    return deploy_version


@task
def build():
    # Retrive app version from app image dockerfile
    deploy_version = _read_tag()

    # Removed previous image with release tag
    try:
        local("docker rmi %s:%s" % (env.WEB_REPOSITORY, env.RELEASE_TAG))
    except:
        print("Previous image not found")

    # Build release image
    local("docker build -t %s %s" % (env.IMAGE_NAME, web_dir))

    # Tag release (master/develop)
    local("docker build -t %s:%s %s" % (env.WEB_REPOSITORY, deploy_version,
                                        web_dir))
    local("docker tag %s:%s %s:%s" % (env.IMAGE_NAME, env.RELEASE_TAG,
                                      env.WEB_REPOSITORY, env.RELEASE_TAG))


@task
def push():
    """
    Push image to registry and cleanup previous release
    """
    deploy_version = _read_tag()

    # Delete previous master from ECR
    try:
        delete_args = {
            "region": env.get("AWS_REGION", "us-east-1"),
            "profile": env.get("AWS_PROFILE")
        }

        delete_command = "aws ecr batch-delete-image --repository-name %s \
            --image-ids imageTag=%s" % (env.IMAGE_NAME, env.RELEASE_TAG)

        for arg in delete_args:
            if not delete_args[arg]:
                continue
            delete_command += " --%s=%s" % (arg, delete_args[arg])

        local(delete_command)
    except:
        print("Remote image tag not found")

    # Push image to repository
    local("docker push %s:%s" % (env.WEB_REPOSITORY, deploy_version))
    local("docker push %s:%s" % (env.WEB_REPOSITORY, env.RELEASE_TAG))


@task
def deploy():
    """
    Deploy the latest image on remote machine
    """
    # Stop web
    container_fabric().stop('web')

    # Pull latest repro changes
    run("docker pull %s:%s" % (env.WEB_REPOSITORY, env.RELEASE_TAG))

    # Update web
    container_fabric().update('web')

    # Start nginx
    container_fabric().startup('nginx')
