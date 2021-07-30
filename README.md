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
  
  And last but not least you can remove an image running **docker image rm** or **docker rmi** folowed by its ID
  
  ### Docker Registries
  
  * Image are stored in registries
  * DockerHub is the most famous one
  * Images name are important because are related with registries
  * Do exist official images and unofficial ones
  * When you pulled ubuntu image, you ran: `docker pull ubuntu` but in theory in a more verbose manner you could run `docker pull docker.io/ubuntu`
  * `docker.io` is the name of the registry hub, dockerhub is the default one so it can be omitted as we did
  * To be honest `ubuntu` is not the image's name but the repo name (on the registry dockerhub) where we pulled a specif version of an image identified by a `TAG`. We omitted tag in pull command (we ran: `docker pull ubuntu`) so docker used as default `latest` value for tag.
  * Supported tag are always showed in the repo page (see [here](https://hub.docker.com/_/ubuntu) for ubuntu)
  * So for example if i need a very old ubuntu version i can use tag `14.04` and run: `docker pull ubuntu:14.04`
  * Summarizing: images' coordinates are defined by:
    * registry name
    * reposiory name
    * image tag
  In this form: `registry_name/repository_name:tag` (e.g. `docker.io/ubuntu:14.04`)
  
  #### Docker Registries Commands
  
  Docker registries commands are basically two (maybe three) and one of them has been already mentioned: **docker pull** it's used to download an image from a registry.
  The second one is **docker push** used to upload an image to a registry. You'd need an account on DockerHub if you want to push an image and after doing that you have to login in your account running **docker login**
  
  ```
  vagrant@docker101:~$ docker login
  Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
  Username: kinderp
  Password: 
  WARNING! Your password will be stored unencrypted in /home/vagrant/.docker/config.json.
  Configure a credential helper to remove this warning. See
  https://docs.docker.com/engine/reference/commandline/login/#credentials-store

  Login Succeeded
  ```
  
  So now let's suppose i want to push ubutu image i've previously pulled to my dckerhub account. Because of images' coordinates depends on repo name (in this case my account on dockerhub) I have to rename my image running **docker tag**
  
  ```
  vagrant@docker101:~$ docker tag ubuntu kinderp/my_ubuntu
  ```
  
  Note that: `kinderp` is my account on dockerhub (repository name on dockerhub in other words). 
  
  You should see this renamed image running:
  
  ```
  vagrant@docker101:~$ docker images
  REPOSITORY          TAG       IMAGE ID       CREATED        SIZE
  kinderp/my_ubuntu   latest    1318b700e415   3 days ago     72.8MB
  ubuntu              latest    1318b700e415   3 days ago     72.8MB
  ubuntu              14.04     13b66b487594   4 months ago   197MB
  ```
  
  Now i'm ready to push ubuntu to my repository running **docker push**:
  
  ```
  vagrant@docker101:~$ docker push kinderp/my_ubuntu
  Using default tag: latest
  The push refers to repository [docker.io/kinderp/my_ubuntu]
  7555a8182c42: Mounted from library/ubuntu 
  latest: digest: sha256:1e48201ccc2ab83afc435394b3bf70af0fa0055215c1e26a5da9b50a1ae367c9 size: 529
  ```
  
  We can now remove this image locally:
  
  ```
  vagrant@docker101:~$ docker image rm kinderp/my_ubuntu
  Untagged: kinderp/my_ubuntu:latest
  Untagged: kinderp/my_ubuntu@sha256:1e48201ccc2ab83afc435394b3bf70af0fa0055215c1e26a5da9b50a1ae367c9
  ```
  
  then verify it has been removed
  
  ```
  vagrant@docker101:~$ docker image ls
  REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
  ubuntu       latest    1318b700e415   3 days ago     72.8MB
  ubuntu       14.04     13b66b487594   4 months ago   197MB
  ```
  
  and finaly re-pull it from your account
  
  ```
  vagrant@docker101:~$ docker pull kinderp/my_ubuntu
  Using default tag: latest
  latest: Pulling from kinderp/my_ubuntu
  Digest: sha256:1e48201ccc2ab83afc435394b3bf70af0fa0055215c1e26a5da9b50a1ae367c9
  Status: Downloaded newer image for kinderp/my_ubuntu:latest
  docker.io/kinderp/my_ubuntu:latest
  ```
  
  ### Building Images
  
  You've learnt that images are composed by different layers and you can see all those with **docker history** showing you commands that created each single layer. 
  
  Let's now see how to create an image.   
  In order to create an image you to have to build it specifying in a special file called `Dockerfile` all the commands that will add a new layer.
  
  A comprehensive list of all possible Dockerfile commands can be found [here](https://docs.docker.com/engine/reference/builder/)
  
  Let's start from an example as simple as possible:
  
  ```Dockerfile
  FROM ubuntu

  LABEL mainteiner="a.caristia@nephila.digital"
 
  RUN apt update -y

  RUN apt install -y netcat

  EXPOSE 8888

  CMD ["nc", "-l", "8888"]
  ```
  
  You can find this file in `examples` dir.
  
  * [`FROM`](https://docs.docker.com/engine/reference/builder/#from): each image has a starting base image (defining its root fs). A valid Dockerfile **MUST START** with a **FROM** instruction
  * [`LABEL`](https://docs.docker.com/engine/reference/builder/#label): as documentation you can add some metadata with **LABEL** instruction
  * [`RUN`](https://docs.docker.com/engine/reference/builder/#run): it runs commands during building phase and (really important) it adds a new layer inside the image.
  * [`EXPOSE`](https://docs.docker.com/engine/reference/builder/#expose): it's a doc instruction informing who's reading that container will expose a specif port but it **DOES NOT EXPOSE** anything. Ports have been exposed once you run a container with **docker run**
  * [`CMD`](https://docs.docker.com/engine/reference/builder/#cmd): it provides a default command to run once spinning image up  as container. You should add only one **CMD** instruction in a Dockerfile and if more are present only the last one will be considered.

So what above Dockerfile does is: running some commands to update ubuntu and intsall nc then informing us 8888 will be exposed at runtime and the defines netcat on port 8888 as default command for each contianer based on this image.

Ok, finally let'd build this image with **docker build**, inside yout lab (`vagrant ssh`) run:

  ```
  cd /vagrant/examples/
  ```

  ```
  docker build -t my-server .
  ```
  
  * `-t`set name and tag of your image, but remember you can always re-tag later with **docker tag**
  * `-f` we didn't use this option but it specifies Dockerfile to use. if omitted docker will expect a `Dockergile` with capital D
  * `.` dot at the end is the **BUILD CONTEXT** and simplyfing it is the location that contains files to be sent to docker deamon. In other words all inside current dir `.` will be sent to docker deamon during building process and they will be present inside the final image. You can use `.dockerignore` to avoid some dir or specific files in the same way you use `.gitignore`  
  
  If building process went well, you should see `my-server` image running:
  
  ```
  vagrant@docker101:/vagrant/examples$ docker image ls
  REPOSITORY          TAG       IMAGE ID       CREATED          SIZE
  my-server           latest    dd122a75be96   58 seconds ago   104MB
  kinderp/my_ubuntu   latest    1318b700e415   3 days ago       72.8MB
  ubuntu              latest    1318b700e415   3 days ago       72.8MB
  ubuntu              14.04     13b66b487594   4 months ago     197MB
  ```
  
### Running Containers

We've finally our new shining image `my-server`, we're ready to spin a container up from that one.

Inside your lab (`vagrant ssh`) run:

  ```
  docker run --name netcat -p 8888:8888 my-server
  ```

  * `--name`: give a nome to new container
  * `p`: publish a container port to the host one (`container_port:host_port`)
  
  Congatulations, your first container is up and running but let's verify that with **docker ps**:
  
  ```
  vagrant@docker101:~$ docker ps
  CONTAINER ID   IMAGE       COMMAND        CREATED              STATUS              PORTS                    NAMES
  17d52393e4bf   my-server   "nc -l 8888"   About a minute ago   Up About a minute   0.0.0.0:8888->8888/tcp   netcat
  ```

  so `netcat` is listening on port 8888 let's talk to it in this way:
  
  ```
  vagrant@docker101:~$ netcat localhost 8888
  ciao sei il mio server?
  ```
  
  you should see the same output on the server side
  
  ```
  vagrant@docker101:~$ docker run --name netcat -p 8888:8888 my-server
  ciao sei il mio server?
  ```
  

### Stopping Containers

It's time to stop your container. Before running **docker stop** you have to get `container_id` with **docker ps**

  ```
  vagrant@docker101:~$ docker ps
  CONTAINER ID   IMAGE       COMMAND        CREATED          STATUS          PORTS                    NAMES
  17d52393e4bf   my-server   "nc -l 8888"   11 minutes ago   Up 11 minutes   0.0.0.0:8888->8888/tcp   netcat
  ```
  
So **docker ps** shows all running containers. If you wanna see all containers even those ones running in the past and died, run **docker ps -a**
But now it's time to die (cit.), let's run:

  ```
  vagrant@docker101:~$ docker stop 17d52393e4bf
  17d52393e4bf
  ```

  You'll see stopped container with **docker ps -a**
  
  ```
  vagrant@docker101:~$ docker ps -a
  CONTAINER ID   IMAGE       COMMAND        CREATED          STATUS                       PORTS     NAMES
  17d52393e4bf   my-server   "nc -l 8888"   21 minutes ago   Exited (137) 2 minutes ago             netcat
  ```

### Starting Containers

You can restart a stopped container with **docker start** knowing as always conteiner_id

  ```
  vagrant@docker101:~$ docker start 17d52393e4bf
  17d52393e4bf
  ```

  ```
  vagrant@docker101:~$ docker ps 
  CONTAINER ID   IMAGE       COMMAND        CREATED       STATUS         PORTS                    NAMES
  17d52393e4bf   my-server   "nc -l 8888"   7 hours ago   Up 2 seconds   0.0.0.0:8888->8888/tcp   netcat
  ```

### Getting inside a container

One of the most useful commands in docker is **docker exec**, using it you can exucute a command inside a contaier.
For example i could run `ps` to knwo which processes are running in a container

  ```
  vagrant@docker101:~$ docker exec 17d52393e4bf ps
      PID TTY          TIME CMD
        1 ?        00:00:00 nc
      111 ?        00:00:00 ps
  ```
  
  an that's correct, we have our server (`netcat` on 8888) and ps ofc over there.
  
  But exec can become even more useful because it permits you to get an interctive shell, just exucute:
  
  ```
  vagrant@docker101:~$ docker exec -it 17d52393e4bf bash
  root@17d52393e4bf:/#
  ```
  
  You're in ;)
  
### Removing Container and Persistent data

You know container are ephemeral but how much they are, let's clarify it.

Let's suppose we have a bash shell gotten as you saw in the previous chapter, what happens if we write a file and then stop and re-start it.

  ```
  root@17d52393e4bf:/# echo "black hole..." > /tmp/entropy 
  root@17d52393e4bf:/# cat /tmp/entropy 
  black hole...
  root@17d52393e4bf:/# exit
  exit
  vagrant@docker101:~$ 
  ```
  
  ```
  vagrant@docker101:~$ docker stop 17d52393e4bf
  17d52393e4bf
  vagrant@docker101:~$ docker start 17d52393e4bf
  17d52393e4bf
  vagrant@docker101:~$ docker exec 17d52393e4bf cat /tmp/entropy
  black hole...
  ```
  
  So data surive to a stop/start process but they don't to a remove command.
  If you remove your container you'll loose all data in it.
  When you write something on a container new layers are added on top of all those (read only) added during building phase. 
  Once you remove a container docker will remove layers written after building phase.
  You can see these layers:
  
  ```
  vagrant@docker101:~$ sudo ls -l /var/lib/docker/overlay2/78932b4f131b8138606a80252a394d36b11ee2ca2dd8018f545f558a298327f6/diff/tmp
  total 4
  -rw-r--r-- 1 root root 14 Jul 30 18:54 entropy
  ```
  
  Layers are stored in your local machine in `/var/lib/docker/overlay2`, `overlay2` is the name of storage driver.
  
  Let's try to remove that container (a running container) with **docker rm**
  
  ```
  vagrant@docker101:~$ docker rm 17d52393e4bf
  Error response from daemon: You cannot remove a running container 17d52393e4bf43ed76e3015104b8779409b53fd2ffbb723bda09bd092a3b88eb. Stop the container before attempting removal or force remove
  ```
  Ok, we can't remove a running container. We could force removing with `docker rm -f 17d52393e4bf` but let's follow the right way.
  
  ```
  vagrant@docker101:~$ docker stop 17d52393e4bf && docker rm 17d52393e4bf
  17d52393e4bf
  17d52393e4bf
  ```
  
  ```
  vagrant@docker101:~$ sudo ls -l /var/lib/docker/overlay2/78932b4f131b8138606a80252a394d36b11ee2ca2dd8018f545f558a298327f6/
  ls: cannot access '/var/lib/docker/overlay2/78932b4f131b8138606a80252a394d36b11ee2ca2dd8018f545f558a298327f6/': No such file or directory
  ```
  
  Our layer has gone, we've lost data :(
  
  
  
  
  
