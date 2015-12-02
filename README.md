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
- `docker-compose up`
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

## TODO: 
- (Done) Try setup with django and postgres
- Try setup with nginx, wsgi, uwsgi
- Try setup with nginx, wsgi, uwsgi and postgres
- Port project to docker
- Try to package a application image
- Try a wp setup

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