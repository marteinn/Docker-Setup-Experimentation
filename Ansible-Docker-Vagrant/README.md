# Ansible+Docker+Vagrant

This is a experiment to see how to provision and transfer images to a vagrant box using ansible.


### Snippets
- Connect to vagrant using ssh
    - `ssh $(vagrant ssh-config | awk '{print " -o "$1"="$2}') localhost` (alt to `vagrant ssh`)

- Transfer local image to remote
    - `docker save <image_id> | bzip2 | ssh $(vagrant ssh-config | awk '{print " -o "$1"="$2}') localhost 'bunzip2 | docker load'`

- Transfer local image to remote (with progress)
    - `docker save <image_id> | bzip2 | pv | ssh $(vagrant ssh-config | awk '{print " -o "$1"="$2}') localhost 'bunzip2 | docker load'`

