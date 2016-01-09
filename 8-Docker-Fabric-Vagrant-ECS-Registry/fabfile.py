import os

from fabric.api import env, local, run, warn_only
from fabric.decorators import task
from fabric.operations import put

from dockerfabric.apiclient import docker_fabric, container_fabric
from dockerfabric import yaml


# Hard coded config vars
ssh_key_path = os.path.join(os.getcwd(), ".vagrant", "machines", "default",
                            "virtualbox", "private_key")
ssh_user = 'vagrant'
web_dir = "django"

docker_map_path = os.path.join(os.getcwd(), "docker_map.yaml")

# Assign env
env.docker_maps = yaml.load_map_file(docker_map_path, 'docker_map')



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
    # Create postgresql data path
    run("mkdir -p /home/%s/var/lib/postgresql/data" % ssh_user)

    # Create postgres db
    container_fabric().startup('db')

    # Create nginx path
    run("mkdir -p /home/%s/var/nginx/conf" % ssh_user)

    # Upload nginx config
    config_path = os.path.join(os.getcwd(), "files", "nginx.conf")
    put(config_path, "/home/%s/var/nginx/conf/nginx.conf" % ssh_user)


@task
def build():
    # Retrive app version from app image dockerfile
    deploy_version = local('cat %s/Dockerfile | \
                           grep -e "^LABEL.version" | \
                           cut -d \\" -f 2' %
                           web_dir, capture=True)

    # Build docker app image
    local("docker build -t %s:%s %s" % (env.WEB_REPOSITORY, deploy_version,
                                        web_dir))


@task
def push():
    # Push image to repository
    local("docker push %s" % env.WEB_REPOSITORY)


@task
def deploy():
    # Start web
    container_fabric().startup('web')

    # Start nginx
    container_fabric().startup('nginx')