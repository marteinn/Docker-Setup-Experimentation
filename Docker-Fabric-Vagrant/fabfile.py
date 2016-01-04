from fabric.api import env
from dockerfabric import tasks as docker

env.docker_tunnel_local_port = 22024  # or any other available port above 1024 of your choice
