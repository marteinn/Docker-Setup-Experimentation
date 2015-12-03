# Docker research

## Tools:
- docker
- docker-machine
- docker-compose
- swarm

## Commands:
### Docker-machine
- `docker-machine ssh default`
- `docker-machine ls`
- Show machine ip
	- `docker-machine ip <name>`
- `eval "$(docker-machine env default)"`

### Docker compose
- Start containers
	- `docker-compose up`
- Run command on container
	- `docker-compose run web django-admin.py startproject composeexample .`
	- `docker-compose run web python manage.py migrate`
- Show containers
	- `docker-compose ps`
- Stop all containers
	- `docker stop $(docker-compose ps -q)`
- Rebuild images
	- `docker-compose build`
- Remove containers
	- `docker rm $(docker-compose ps -q)`

### Docker
- Show running containers
	- `docker ps`
- Stop all containers
	- `docker stop $(docker ps -a -q)`
- Show all images
	- `docker images`
- Remove all images
	- `docker rmi $(docker images -q)`
- Remove all containers
	- `docker rm $(docker ps -a -q)`
- Remove all dangling images
	- `docker images -q --filter "dangling=true" | xargs docker rmi`
- Remove all stopped containers: 
	- `docker rm $(docker ps -a -q)`
- Remove image
	- `docker rmi <image id>`
- Build image
	- `docker build <imagename>`
- Run container in shell
	- `docker exec -it <container_id> bash`
- Run command on container
	- Example: `docker exec <container_id> django-admin.py startproject composeexample .`
	- Example: `docker exec <container_id> web python manage.py migrate`

## TODO: 
- (Done) Try setup with django and postgres
- (Done) Try setup with nginx, wsgi, uwsgi
- (Done) Try to package a application image
- (Done) Try setup with nginx, django, uwsgi and postgres
- (Done) Port a django project to docker
- Test to run a multisite setup with reverse proxy
- Port a wp project to docker
- Research docker repository

## Questions:
- Best practice when distributing files?
- How do I mount files to a image correctly?
- How do I perform Django migrations in a docker image?
	- Wrap migrate and web serve in a bash script called `docker-entrypoint.sh`
- Best practice when dealing with log-files?
- Best approach when debugging?
- How can I connect to a container directly?
	- `docker exec -it <container_id> bash`	

## Experiment: 

## References
- https://docs.docker.com/engine/articles/dockerfile_best-practices/
- https://github.com/dockerfiles/django-uwsgi-nginx/blob/master/Dockerfile
- https://github.com/b00giZm/docker-compose-nodejs-examples/blob/master/05-nginx-express-redis-nodemon/docker-compose.yml
- http://anandmanisankar.com/posts/docker-container-nginx-node-redis-example/
- https://docs.docker.com/engine/articles/dockerfile_best-practices/
- https://docs.docker.com/mac/step_one/
- https://docs.docker.com/v1.8/installation/mac/
- http://crosbymichael.com/dockerfile-best-practices.html
- http://docs.docker.com/engine/userguide/networking/default_network/dockerlinks/#connect-with-the-linking-system
- http://michal.karzynski.pl/blog/2015/04/19/packaging-django-applications-as-docker-container-images/
- https://github.com/jwilder/nginx-proxy
- http://jasonwilder.com/blog/2014/03/25/automated-nginx-reverse-proxy-for-docker/
- http://eyenx.ch/2015/04/18/loadbalancing-containers-with-docker-compose/
- https://realpython.com/blog/python/django-development-with-docker-compose-and-machine/