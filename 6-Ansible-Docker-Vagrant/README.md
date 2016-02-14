# 6. Ansible+Docker+Vagrant

This is a experiment to see how to provision and transfer images to a vagrant box using ansible.


### Playbooks

- prepare_server.yml
    - Installs aufs driver for ubuntu
    - Hardens the server (firewall, auth...)
    - Installs docker
- setup.yml
    - Download and start postgres container
    - Add config for nginx
- deploy.yml
    - Retrive app version
    - Build app image
    - Transfer app image to remote
    - Stop and remove previous app container
    - Tag new image as 'latest'
    - Clear up old releases
    - Start app container
    - Start/restart nginx container


### Snippets
- Connect to vagrant using ssh
    - `ssh $(vagrant ssh-config | awk '{print " -o "$1"="$2}') localhost` (alt to `vagrant ssh`)

- Transfer local image to remote
    - `docker save <image_id> | bzip2 | ssh $(vagrant ssh-config | awk '{print " -o "$1"="$2}') localhost 'bunzip2 | docker load'`

- Transfer local image to remote (with progress)
    - `docker save <image_id> | bzip2 | pv | ssh $(vagrant ssh-config | awk '{print " -o "$1"="$2}') localhost 'bunzip2 | docker load'`

- Run deploy playbook
```
ansible-playbook ./ansible/deploy.yml -i .vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory -u vagrant
```

- Ping vagrant machine
```
ansible all -m ping -i .vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory -u vagrant
```

## References

#### Docker save/load
- https://opensolitude.com/2015/05/26/building-docker-images-with-ansible.html
- https://realguess.net/2015/02/04/docker-save-load-and-deploy/
- http://tuhrig.de/difference-between-save-and-export-in-docker/

#### Provisioning
- http://www.hiddentao.com/archives/2014/06/03/shippable-ansible-docker-loggly-for-awesome-deployments/

#### Alt deployment procedures
- http://blog.ionic.io/docker-hot-code-deploys/
