# docker101

### Playground

We'll use vagrant in order to obtain a clean environment as lab where we'll be free to play with docker without any fear to break our dev env. 
So before doing anything you shuold:

* Install `virtualbox`
* Install `vagrant`

#### Start lab

* Clone this repo: `git clone git@github.com:kinderp/docker101.git`
* move to `ubuntu` dir: `cd docker101/playground/ubuntu/`
* Run: `vagrant up` and wait
* Ssh into vm: `vagrant ssh`
* Check if docker has been provisioned correctly
   * `systemctl status docker`
   * `docker ps`

#### Stop lab

* `vagrant halt` 

#### Suspend - Resume lab

* `vagrant suspend`
* `vagrant resume`

#### Destroy lab

Lab takes space on disk so it's a good idea removing it after your training session.

* Before destroying lab please check if it exists:
  ```
  VBoxManage list vms|grep nephila
  "nephila_ubuntu" {9e6b0cee-9a45-4c50-83fd-8809b21075a1}
  ```
* `vagrant destroy`
* You shouldn't get any output now running: `VBoxManage list vms|grep nephila`
* `vagrant destroy`

## Introduction

TODO

### Docker Architecture

TODO

#### docker client

TODO

#### docker engine

TODO

#### containerd and others container runtimes

TODO

### Docker Images

* An image is a read‑only template for creating containers. 
* It contains all the code to run an application. 
* Images are build‑time constructs while containers are runtime contropart. 
* A container is a running image. If it helps you, it's something similar to relathionship between a program and a process. 
* Deeping dive into image we can say an image is composed by a bunch of layer (read-only) stacked together but trasparent to us thanks to kernel union filesystem feature
* So for simplicity you can think of union fs as a bunch of read‑only file systems or block devices with a writeable layer on top, and presenting them to the system as a unique layer.
* In order to track which layers belong to an image a Manifest file is used.
* The manifest is a JSON file explaining how all different layers fits together. 
* An image is a bunch of layers that are stacked on top of each other. but it looks and feels like a unified file system, like a single flat image. 
* Layer funcionality is really important for space disk consumption because in that way different containers can share layers with each others.

#### Docker Images Commands

Images are stored in registries on the web, so first af all you have to download image you need with **docker pull**.
Inside your lab (`vagrant ssh`) let's run this:

  ```
  docker pull ubuntu
  ```

  You should see something like this:
  
  ```
  vagrant@docker101:~$ docker pull ubuntu
  Using default tag: latest
  latest: Pulling from library/ubuntu
  16ec32c2132b: Pull complete 
  Digest: sha256:82becede498899ec668628e7cb0ad87b6e1c371cb8a1e597d83a47fac21d6af3
  Status: Downloaded newer image for ubuntu:latest
  docker.io/library/ubuntu:latest
  ```
  
  Now you have ubuntu image in your disk and you can verify that's true just running **docker images ls** or simply **docker images**
  
  ```
  docker images ls
  ```
  
  ```
  vagrant@docker101:~$ docker images
  REPOSITORY   TAG       IMAGE ID       CREATED      SIZE
  ubuntu       latest    1318b700e415   3 days ago   72.8MB
  ```

  As you can see above an image has a `TAG` and an `ID`. Id ofc identifies uniquely that image while tag is used to distinguish different versions (usually different releases of the code)
  
  Once you have an image you can run containers from that.(we'll later how to do)
  If you're wondering where these stuffs are stored in your disk, it depends on the storage driver: `/var/lib/docker` and the name of the driver, in my case:
  
  ```
  vagrant@docker101:~$ sudo ls -l /var/lib/docker/overlay2/
  total 8
  drwx------ 3 root root 4096 Jul 30 07:17 8986a619617ea9f23266140e6e45ad8a25b0d443dca935dfe023e585c461ce3c
  ```
  
  that one is the base (and only layer) in other words it's the ubuntu root fs:
  
  ```
  vagrant@docker101:~$ sudo ls /var/lib/docker/overlay2/8986a619617ea9f23266140e6e45ad8a25b0d443dca935dfe023e585c461ce3c/diff/etc
  adduser.conf		cron.d		deluser.conf  gai.conf	 hosts	    ld.so.cache    login.defs	networks       pam.d	  rc1.d  rc6.d	      selinux  subuid	    update-  motd.d
  alternatives		cron.daily	dpkg	      group	 init.d     ld.so.conf	   logrotate.d	nsswitch.conf  passwd	  rc2.d  rcS.d	      shadow   sysctl.conf  xattr.conf
  apt			debconf.conf	e2scrub.conf  gshadow	 issue	    ld.so.conf.d   lsb-release	opt	       profile	  rc3.d  resolv.conf  shells   sysctl.d
  bash.bashrc		debian_version	environment   host.conf  issue.net  legal	   machine-id	os-release     profile.d  rc4.d  rmt	      skel     systemd
bindresvport.blacklist	default		fstab	      hostname	 kernel     libaudit.conf  mke2fs.conf	pam.conf       rc0.d	  rc5.d  security     subgid   terminfo
  ```
  
  So summarizing, an image is composed by differnt layers (read-only) that are stored in a specific path of your disk and are showed as an unique flat layer.
  
  You can use **docker history** to know which commands were used to build an image (and so to add each different layers)
  
  ```
  agrant@docker101:~$ docker history 1318b700e415
  IMAGE          CREATED      CREATED BY                                      SIZE      COMMENT
  1318b700e415   3 days ago   /bin/sh -c #(nop)  CMD ["bash"]                 0B        
  <missing>      3 days ago   /bin/sh -c #(nop) ADD file:524e8d93ad65f08a0…   72.8MB 
  ```
  
  the last one at the bottom is the root fs layer, on top of it there's a layer (size 0B) to run a shell once an image will be run as container.
  `CMD` is one of directive used in `Dockerfile` that will see later. So far you have just to know: if you images is too big, docker inspect
  can help you to know which layers are taking too space.
  
  Remember if you need more specific infos about an image you can use **docker inspect <image_id>**. 
