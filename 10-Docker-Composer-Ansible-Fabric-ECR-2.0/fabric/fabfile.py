import os

from fabric.api import env, local, run
from fabric.decorators import task
from fabric.operations import put


# Hard coded config vars
ssh_user = 'vagrant'
web_dir = "../src"


compose_env_files = [
    'web.env',
    'db.env',
]

compose_files = [
    'docker-compose-prod.yml'
]

compose_config = ""
for arg in compose_files:
    compose_config += " -f %s" % arg

compose_config = compose_config.strip()


@task
def vagrant():
    ssh_key_path = os.path.join(os.getcwd(), "..", "ansible", ".vagrant",
                                "machines", "default", "virtualbox",
                                "private_key")
    env.user = 'vagrant'
    env.hosts = ['127.0.0.1:2222']
    env.key_filename = ssh_key_path


@task
def test():
    run('uname -a')


@task
def sync_compose_envs():
    for env_file in compose_env_files:
        env_path = os.path.join(os.getcwd(), '..', 'docker-compose-config',
                                env_file)
        put(env_path, "/home/%s/docker-compose-config/%s" % (ssh_user,
                                                             env_file))


@task
def sync_compose_config():
    for config_file in compose_files:
        config_path = os.path.join(os.getcwd(), '..', config_file)
        put(config_path, "/home/%s/%s" % (ssh_user, config_file))


@task
def setup(up=False):
    # Login to remote repro
    _aws_ecr_login(run, region=env.get("AWS_REGION", "us-east-1"))

    # Create compose config files
    run("mkdir -p /home/%s/docker-compose-config" % ssh_user)

    # Upload docker-compose files
    sync_compose_config()
    sync_compose_envs()

    # Create postgresql data path
    run("mkdir -p /home/%s/var/lib/postgresql/data" % ssh_user)

    # Create nginx path
    run("mkdir -p /home/%s/var/nginx/conf" % ssh_user)

    # Create stub web app config
    run("mkdir -p /home/%s/var/web/" % ssh_user)
    run("touch /home/%s/var/web/.env" % ssh_user)
    run("touch /home/%s/var/web/uwsgi.log" % ssh_user)

    # Upload nginx config
    config_path = os.path.join(os.getcwd(), "files", "nginx.conf")
    put(config_path, "/home/%s/var/nginx/conf/nginx.conf" % ssh_user)

    # Do initial compose setup
    # run("docker-compose -f %s up -d -p %s" % (compose_config, env.PROJECT_NAME))


def _read_tag():
    # Retrive app version from app image dockerfile
    deploy_version = local('cat %s/Dockerfile | \
                           grep -e "^LABEL.version" | \
                           cut -d \\" -f 2' %
                           web_dir, capture=True)

    return deploy_version


def _aws_ecr_login(method, region="us-east-1", profile=""):
    # Authenticate with ecr
    auth_args = {
        "region": region,
        "profile": profile
    }

    auth_command = "aws ecr get-login"

    for arg in auth_args:
        if not auth_args[arg]:
            continue
        auth_command += " --%s=%s" % (arg, auth_args[arg])

    method("$(%s)" % auth_command)


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

    # Authenticate with ecr
    _aws_ecr_login(local, region=env.get("AWS_REGION", "us-east-1"),
                   profile=env.get("AWS_PROFILE"))

    # Push image to repository
    local("docker push %s:%s" % (env.WEB_REPOSITORY, deploy_version))
    local("docker push %s:%s" % (env.WEB_REPOSITORY, env.RELEASE_TAG))


@task
def deploy():
    _aws_ecr_login(run, region=env.get("AWS_REGION", "us-east-1"))

    # Pull latest repro changes
    run("docker pull %s:%s" % (env.WEB_REPOSITORY, env.RELEASE_TAG))

    # Restart web container
    run("docker-compose %s -p %s up -d" % (compose_config, env.PROJECT_NAME))
    # run("docker-compose %s restart" % compose_config)
    # run("docker-compose %s restart nginx" % compose_config)

    # TODO: Remove unused images
    # https://forums.docker.com/t/command-to-remove-all-unused-images/20/5
    #try:
        #run('docker rmi -f $(docker images | grep "<none>" | awk "{print \$3}")')
    #except:
        #pass
