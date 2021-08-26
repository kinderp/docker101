
Table of Contents
=================


   * [Playground](#playground)
       * [Start lab](#start-lab)
       * [Stop lab](#stop-lab)
       * [Suspend - Resume lab](#suspend---resume-lab)
       * [Destroy lab](#destroy-lab)
   * [Introduction](#introduction)
      * [Docker Architecture](#docker-architecture)
         * [docker client](#docker-client)
         * [docker engine](#docker-engine)
         * [containerd and others container runtimes](#containerd-and-others-container-runtimes)
      * [Docker Images](#docker-images)
         * [Docker Images Commands](#docker-images-commands)
      * [Docker Registries](#docker-registries)
         * [Docker Registries Commands](#docker-registries-commands)
      * [Building Images](#building-images)
      * [Running Containers](#running-containers)
      * [Stopping Containers](#stopping-containers)
      * [Starting Containers](#starting-containers)
      * [Getting inside a container](#getting-inside-a-container)
      * [Removing Container and Persistent data](#removing-container-and-persistent-data)
      * [Volumes](#volumes)
         * [Attaching a volume](#attaching-a-volume)
      * [Let's dirty our hands with volumes](#lets-dirty-our-hands-with-volumes)
      * [Docker Network](#docker-network)
   * [Docker Compose](#docker-compose)
      * [Let's dirty our hands with docker-compose](#lets-dirty-our-hands-with-docker-compose)
      * [Docker-compose commands](#docker-compose-commands)


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
* Check if docker has been correctly provisioned
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

![](https://github.com/kinderp/docker101/blob/master/images/vm_vs_container.jpeg)

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
* Images are build‑time constructs while containers are its runtime contropart. 
* A container is a running image. If it helps you, it's something similar to relathionship between a program and a process. 
* Deeping dive into image we can say an image is composed by a bunch of layer (read-only) stacked together but trasparent to us thanks to kernel `union filesystem` feature
* So for simplicity you can think of union fs as a bunch of read‑only file systems or block devices with a writeable layer on top (created only once a container is spinned up), and presenting them to the system as a unique layer.
* In order to track which layers belong to an image a Manifest file is used.
* The manifest is a JSON file explaining how all different layers fit together. 
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
  
  Now you have an ubuntu image in your disk and you can verify it just running **docker image ls** or simply **docker images**
  
 
  ```
  vagrant@docker101:~$ docker images
  REPOSITORY   TAG       IMAGE ID       CREATED      SIZE
  ubuntu       latest    1318b700e415   3 days ago   72.8MB
  ```

  As you can see above an image has a `TAG` and an `ID`. 

  Id identifies uniquely an image while tag is used to distinguish different versions (usually different releases of the code)
  
  Once you have an image you can run containers from that (we'll see later how to do)

  If you're wondering where these stuffs are stored in your disk, it depends on the storage driver: `/var/lib/docker`, in my case:
  
  ```
  vagrant@docker101:~$ sudo ls -l /var/lib/docker/overlay2/
  total 8
  drwx------ 3 root root 4096 Jul 30 07:17 8986a619617ea9f23266140e6e45ad8a25b0d443dca935dfe023e585c461ce3c
  ```
  
  that one above is the base (and only layer) or in other words it's the ubuntu root fs:
  
  ```
  vagrant@docker101:~$ sudo ls /var/lib/docker/overlay2/8986a619617ea9f23266140e6e45ad8a25b0d443dca935dfe023e585c461ce3c/diff/etc
  adduser.conf		cron.d		deluser.conf  gai.conf	 hosts	    ld.so.cache    login.defs	networks       pam.d	  rc1.d  rc6.d	      selinux  subuid	    update-  motd.d
  alternatives		cron.daily	dpkg	      group	 init.d     ld.so.conf	   logrotate.d	nsswitch.conf  passwd	  rc2.d  rcS.d	      shadow   sysctl.conf  xattr.conf
  apt			debconf.conf	e2scrub.conf  gshadow	 issue	    ld.so.conf.d   lsb-release	opt	       profile	  rc3.d  resolv.conf  shells   sysctl.d
  bash.bashrc		debian_version	environment   host.conf  issue.net  legal	   machine-id	os-release     profile.d  rc4.d  rmt	      skel     systemd
bindresvport.blacklist	default		fstab	      hostname	 kernel     libaudit.conf  mke2fs.conf	pam.conf       rc0.d	  rc5.d  security     subgid   terminfo
  ```
  
  So summarizing, an image is composed by differnt layers (read-only) that are stored in a specific path of your disk but are showed as an unique flat layer.
  
  You can use **docker history** to know which commands were used to build an image (and so each different layers)
  
  ```
  agrant@docker101:~$ docker history 1318b700e415
  IMAGE          CREATED      CREATED BY                                      SIZE      COMMENT
  1318b700e415   3 days ago   /bin/sh -c #(nop)  CMD ["bash"]                 0B        
  <missing>      3 days ago   /bin/sh -c #(nop) ADD file:524e8d93ad65f08a0…   72.8MB 
  ```
  
  the last one at the bottom is the root fs layer, on top of it there's a layer (size 0B) to execute a shell once an image will be run as container.
  `CMD` is one of directives used in `Dockerfile` that will see later. So far you have just to remember: if your images is too big, **docker history**
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
  
  So now let's suppose i want to push ubutu image (that one i've previously pulled in) to my dckerhub account. Because of images' coordinates depends on repo name (in this case my account on dockerhub) I have to rename my image running **docker tag**
  
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
  
  and then verify that it has been removed
  
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
  
  You've learnt that images are composed by different layers and you can see all those with **docker history** showing you commands that added each single layer
  
  Let's now see how to create an image   

  In order to create an image you to have to build it specifying in a special file called `Dockerfile` all the commands that will add a new layer.
  Some commands don't add any layers (you'll see 0B for that virtual layer) anyway.
  
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
  * [`CMD`](https://docs.docker.com/engine/reference/builder/#cmd): it provides a default command to be executed once spinning image up  as container. You should add only one **CMD** instruction in a Dockerfile and if more than one are present only the last one will be considered.

So what above Dockerfile does is: running some commands to update ubuntu and intsall nc then informing us 8888 will be exposed at runtime and then it sets netcat on port 8888 as default command for each contianer based on this image.

Ok, finally let'd build this image with **docker build**, inside yout lab (`vagrant ssh`) run:

  ```
  cd /vagrant/examples/
  ```

  ```
  docker build -t my-server .
  ```
  
  * `-t`set name and tag of your image, but remember you can always re-tag later with **docker tag**
  * `-f` we didn't use this option but it specifies the filename of Dockerfile to use. if omitted docker will expect a filename named as: `Dockergile` with capital D
  * `.` dot at the end is the **BUILD CONTEXT** and simplyfing it is the location that contains files to be sent to docker deamon. In other words everything inside current dir `.` will be sent to docker deamon during building process and they will be present inside the final image. You can use `.dockerignore` to avoid including some dir or specific files in the same way you use `.gitignore`  
  
  If building process went well, you should see `my-server` image:
  
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
  * `-p`: publish a container port to the host one (`container_port:host_port`). if you remember we used `EXPOSE` in `Dockerfile` to document we'll expose 8888 in run command. A port is expoed only in run command (running phase) not before inside a Dockerfile (building phase).
  
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

You can restart a stopped container with **docker start** knowing as always its conteiner_id

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
For example i could run `ps` to know which processes are running in a container

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
  When you write something on a container new layers (writable layers) are added on top of all those (read only) added during building phase. 
  Once you remove a container docker will remove layers written after building phase.
  You can see these layers:
  
  ```
  vagrant@docker101:~$ sudo ls -l /var/lib/docker/overlay2/78932b4f131b8138606a80252a394d36b11ee2ca2dd8018f545f558a298327f6/diff/tmp
  total 4
  -rw-r--r-- 1 root root 14 Jul 30 18:54 entropy
  ```
  
  Layers are stored in your local machine in `/var/lib/docker/overlay2`, `overlay2` is the name of the storage driver.
  
  Let's try to remove that container (a running container) with **docker rm**
  
  ```
  vagrant@docker101:~$ docker rm 17d52393e4bf
  Error response from daemon: You cannot remove a running container 17d52393e4bf43ed76e3015104b8779409b53fd2ffbb723bda09bd092a3b88eb. Stop the container before attempting removal or force remove
  ```
  Ok, we can't remove a running container. We could force its removing with `docker rm -f 17d52393e4bf` but let's follow the right way.
  
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
  
    
 ### Volumes
 
 What we've learnt so far is: each container gets its **non persistent storage** and it's managed by storage driver but you loose all after removing the container.
 In order to obtain **persistent storage** you have to use volumes.

 A volume is an external storage that you can attach to a container and because of it's external to a container it persists after you remove container at which it's attached.
 
 You can create a volume before running a container with **docker volume crete**
 
   ```
   vagrant@docker101:~$ docker volume create one
   one
   ```
   
And showing all existing volumes with **docker volume ls**

  ```
  vagrant@docker101:~$ docker volume ls
  DRIVER    VOLUME NAME
  local     one
  ```
  
You can get more infos about volumes you created with **docker volume inspect**, for example you can get local path where it's saved

  ```
  vagrant@docker101:~$ docker volume inspect one
  [
      {
          "CreatedAt": "2021-08-01T15:53:48Z",
          "Driver": "local",
          "Labels": {},
          "Mountpoint": "/var/lib/docker/volumes/one/_data",
          "Name": "one",
          "Options": {},
          "Scope": "local"
      }
  ]
  ```
  
And yon can delete a volume with **docker volume rm**

  ```
  vagrant@docker101:~$ docker volume rm one
  one

  vagrant@docker101:~$ docker volume ls
  DRIVER    VOLUME NAME
  ```

As you maybe already noticed volumes are indipendent objects and they are related with a container just during time they are attached to a container. After the container dies a volume continue to exist and can be used/attached to a new container providing a good way to implement persistent storage.

#### Attaching a volume

Let's see now how to attach a volume to a container using **docker run**. 

In otder to do that we can use `--mount` option specifying the source (the volume name) and the target (the mountpoint inside container's fs)

  ```
  vagrant@docker101:~$ docker run -dit --name attach_volume --mount source=my_volume,target=/my_persistent_dir ubuntu
  dd1d107be88e6f3c4e9a88e838e6f6979812d99930b29b6e5c9460c7bc7ccc2b
  ```

volume `my_volume` will be created if it does not exist.

A new container named `attach_volume` exists and a volume `my_volume` has been created and attached to it

  ```
  vagrant@docker101:~$ docker ps
  CONTAINER ID   IMAGE     COMMAND   CREATED              STATUS              PORTS     NAMES
  dd1d107be88e   ubuntu    "bash"    About a minute ago   Up About a minute             attach_volume

  vagrant@docker101:~$ docker volume ls
  DRIVER    VOLUME NAME
  local     my_volume
  vagrant@docker101:~$ 
  ```
  
  Not let's try to write something inside `my_persistent_dir` then remove the container and re-attach the same volume to a new one
  
  ```
  vagrant@docker101:~$ docker exec -it dd1d107be88e bash
  root@dd1d107be88e:/# echo "i will survive" > /my_persistent_dir/test.txt
  root@dd1d107be88e:/# cat /my_persistent_dir/test.txt 
  i will survive
  ```
  
  Remove all
  
  ```
  vagrant@docker101:~$ docker ps
  CONTAINER ID   IMAGE     COMMAND   CREATED          STATUS          PORTS     NAMES
  dd1d107be88e   ubuntu    "bash"    15 minutes ago   Up 15 minutes             attach_volume

  vagrant@docker101:~$ docker rm dd1d107be88e
  Error response from daemon: You cannot remove a running container dd1d107be88e6f3c4e9a88e838e6f6979812d99930b29b6e5c9460c7bc7ccc2b. Stop the container before  attempting removal or force remove
  ```
  
  Dokcer does not permit you to remove a container with an attached volume, that's good but this time let's force docker to do that in this way:
  
  ```
  vagrant@docker101:~$ docker rm -f dd1d107be88e
  dd1d107be88e

  vagrant@docker101:~$ docker ps
  CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
  ```
  
  Container is died, let's create a new one with the same old volume attached to it
  
  ```
  vagrant@docker101:~$ docker run -dit --name new_container --mount source=my_volume,target=/whatever alpine
  Unable to find image 'alpine:latest' locally
  latest: Pulling from library/alpine
  5843afab3874: Pull complete 
  Digest: sha256:adab3844f497ab9171f070d4cae4114b5aec565ac772e2f2579405b78be67c96
  Status: Downloaded newer image for alpine:latest
  240af3f227538d08f1ff265d5acfc242d6548d5ee7680a15357836c9ae0225c8
  ```
  
  As you can see above you can change `target` mountpoint, container name and image but result will be the same: our `my_volume` volume will be attached to the new container, let's verify it.
  
  ```
  vagrant@docker101:~$ docker ps
  CONTAINER ID   IMAGE     COMMAND     CREATED         STATUS         PORTS     NAMES
  240af3f22753   alpine    "/bin/sh"   2 minutes ago   Up 2 minutes             new_container

  vagrant@docker101:~$ docker exec 240af3f22753 cat /whatever/test.txt
  i will survive
  ```

### Let's dirty our hands with volumes
  
When you think about volumes and persistent data you probably associate it with a database.
Let's try to run a postgres container attaching pgdata folder to an external volume in otder to be able to make indipendet our data to the lifecycle of the container.

  ```
  vagrant@docker101:~$ docker volume create pgdata
  pgdata

  vagrant@docker101:~$ docker volume ls
  DRIVER    VOLUME NAME
  local     my_volume
  local     pgdata

  ```

  ```
  vagrant@docker101:~$ docker run -it --rm -v pgdata:/var/lib/postgresql/data -e POSTGRES_PASSWORD=mysecretpassword postgres
  ```
  
  ```
  vagrant@docker101:~$ docker ps|grep postgres
  e3d0985a6993   postgres   "docker-entrypoint.s…"   2 minutes ago    Up 2 minutes    5432/tcp   cool_engelbart
  ```
  
  Did you notice? We used another options `-v` to create/attach a container in `run` command. You can use both `--mount` or `-v`, [here](https://docs.docker.com/storage/volumes/#choose-the--v-or---mount-flag) some infos about this double options
  
  Now we wanna try to connect to postgres but wait a second we didn't open any port (`-p` options in `docker run` command) so we can't use `psql` from our local machine because there's no mapping between a local port and a container one. We'll do it later but for now we can just start a new container and run from there `psql`. 
  
  
  ```
  vagrant@docker101:~$ docker run -it --rm postgres bash
  root@f7da5d8f4580:/# psql -h 172.17.0.3 -U postgres
  Password for user postgres: 
  psql (13.3 (Debian 13.3-1.pgdg100+1))
  Type "help" for help.

  postgres=# 
  ```
  
  Cool, but wait a second where did we get postgres ip to connect to?
  I used **docker inspect** to retrieve ip of running postgres container in this way:

  ```
  vagrant@docker101:~$ docker ps|grep postgres
  e3d0985a6993   postgres   "docker-entrypoint.s…"   23 minutes ago   Up 23 minutes   5432/tcp   cool_engelbart

  vagrant@docker101:~$ docker inspect e3d0985a6993|grep IPAddress
            "SecondaryIPAddresses": null,
            "IPAddress": "172.17.0.3",
                    "IPAddress": "172.17.0.3",

  ```
  
  We're happy but not too much because we can't connect to postgres directly from our local machine, in order to do that we have to remove running container and use `-p` option to bint local port to a conatiner one. We won't loose our data because pgdata dir has been attached to an external volume. 
  
  ```bash
  vagrant@docker101:~$ docker rm -f $(docker ps -q)
  e3d0985a6993
  240af3f22753
  
  vagrant@docker101:~$ docker ps
  CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
  
  vagrant@docker101:~$ docker run -it --rm -p 6789:5432 --mount source=pgdata,target=/var/lib/postgresql/data -e POSTGRES_PASSWORD=mysecretpassword postgres
  
  vagrant@docker101:~$ sudo apt install -y postgresql-client

  vagrant@docker101:~$ psql -h localhost -p 6789 -U postgres
  Password for user postgres: 
  psql (12.7 (Ubuntu 12.7-0ubuntu0.20.04.1), server 13.3 (Debian 13.3-1.pgdg100+1))
  WARNING: psql major version 12, server major version 13.
         Some psql features might not work.
  Type "help" for help.

  postgres=#
  ```
  
  First of all `docker rm -f $(docker ps -q)` it's a useful trick to remove all the running containers.
  In `psql -h localhost -p 6789 -U postgres` we connected to running postgres container using localhost and the number of mapped port used in `-p` option of run command. It worked but take in consideration that postgres container is attached to a docker network and it has it own ip (as you've seen before) so I could obtain the same result even if we'd have retrieved that ip with `docker inspect 30b3896cc16b|grep IPAddress` and then `psql -h 172.17.0.2 -p 5432 -U postgres`. We'll talk about docker network in the next chapter
  
  
 ### Docker Network
 
 In our discussion we've already mentioned docker networks, you've already seen that each docker container has its own ip. and you can get this ip running **docker inspect**.
 
 Docker has a series of specific commands for managing networks of containers: **docker network**.
 
 As first command, we can list existing networks with **docker network ls**.
 
 So inside your lab (`vagrant ssh`):
 
   ```
   vagrant@docker101:~$ docker network ls
   NETWORK ID     NAME      DRIVER    SCOPE
   fc58c3aa8544   bridge    bridge    local
   fce7f90499c1   host      host      local
   757ad1104099   none      null      local
   ```

Let's see in details the first one named: `brigde`, its name is not casual, as you maybe know bridges are network devices working at layer 2 connecting two Ethernet segments together. Linux kernel (if bridging is enabled) can create/mange virtual bridges usually providing a cli interface to sysadmin through `brctl` command. If you run in your lab:

  ```
  vagrant@docker101:~$ brctl show
  bridge name	bridge id		STP enabled	interfaces
  docker0		8000.0242e47410f2	no		vethf0aa088
  ```
  
docker during its installation has created `docker0` bridge for you and it will be used as device for `bridge` networks.
Bridge is the dafault network in docker and every new containers will be added in this network but ofc you can always specify a different network for a new container.
Bridge networks have a local scope (`SCOPE` column in `docker network ls`) that means they can connect containers only inside a single host, furthermore a bridge network is isolated: a container inside a bridge network can't talk with another container in a different bridge network even if they resides in the same host.
If you wanna connect to a container inside a bridge network from the outside workd you have to use port mapping as describe in the previous chapters.

If you need to connect each others containers in different hosts you have to use `overlay` networks, these kind of networks are multiple hosts networks.
Bridge network is just an isolated bridge scoped to a single host while overlay is a single layer2 bridge network spanning multiple hosts and it doesn't matter if hosts are inside different (physical network) containers will stay in the same (virtual) network.

The only issue with overlay networks is that they are containers only network, if you need to connect containers to VM(s) or physical servers you have to use `macvlan` networks. In a macvlan network containers have its ip and mac address on the existing network and that permits containers to be visivile in your lan without any bridge or port mapping.

After this breif digression about networks types in docker let's inspect our default bridge network with **docker network inspect**

  ```
  vagrant@docker101:~$ docker network inspect bridge
  [
    {
        "Name": "bridge",
        "Id": "fc58c3aa85440af16c381a7bfe975b2ff81fab1b814ed91ee53683aaf4d3a334",
        "Created": "2021-07-30T06:46:37.545472917Z",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "172.17.0.0/16",
                    "Gateway": "172.17.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {},
        "Options": {
            "com.docker.network.bridge.default_bridge": "true",
            "com.docker.network.bridge.enable_icc": "true",
            "com.docker.network.bridge.enable_ip_masquerade": "true",
            "com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
            "com.docker.network.bridge.name": "docker0",
            "com.docker.network.driver.mtu": "1500"
        },
        "Labels": {}
    }
]

  ```
  
  Cool, it has its subnet (`"172.17.0.0/16`) gateway (`172.17.0.`) but no containers.
  
  Let's try to add a new container to the default bridge network
  
  ```
  vagrant@docker101:~$ docker run -d --rm --name network_container ubuntu sleep 1000
  1f929596d974e02c5ceb48c2a357c3eef435305962bebb8f11adeae8d124610b
  
  vagrant@docker101:~$ docker ps
  CONTAINER ID   IMAGE     COMMAND        CREATED         STATUS         PORTS     NAMES
  1f929596d974   ubuntu    "sleep 1000"   5 seconds ago   Up 5 seconds             network_container
  
  vagrant@docker101:~$ docker network inspect bridge|grep -A 4 -B 2 network_container 
        "Containers": {
            "1f929596d974e02c5ceb48c2a357c3eef435305962bebb8f11adeae8d124610b": {
                "Name": "network_container",
                "EndpointID": "7b7fddaf4d4e26e78671c5ca4f2012d31c4c00f1468dd07bfa661d3cff3a6475",
                "MacAddress": "02:42:ac:11:00:02",
                "IPv4Address": "172.17.0.2/16",
                "IPv6Address": ""

  ```
  
  
And you can ping container as any host in your lan

  ```
  vagrant@docker101:~$ ping 172.17.0.2
  PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
  64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.167 ms
  64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.103 ms
  ^C
  --- 172.17.0.2 ping statistics ---
  2 packets transmitted, 2 received, 0% packet loss, time 1001ms
  rtt min/avg/max/mdev = 0.103/0.135/0.167/0.032 ms

  ```
  
It works even with a different new network, so let's create a new bridge network:

  ```
  vagrant@docker101:~$ docker network create --driver bridge my_network
  4032cd4d89fedf783f36fa74ad2b7f6214a0b415133e1aea4a5299451b0cb5ae

  vagrant@docker101:~$ docker network ls|grep my_network
  4032cd4d89fe   my_network   bridge    local

  vagrant@docker101:~$ docker run -d --rm --network my_network --name container_in_my_network alpine sleep 1000
  60a137aa23c7b1e5c42a5e54019a1d50cb7eda68f2701cb100a546f713f33aaa

  vagrant@docker101:~$ docker network inspect my_network|grep -A 4 -B 2 in_my_network
        "Containers": {
            "60a137aa23c7b1e5c42a5e54019a1d50cb7eda68f2701cb100a546f713f33aaa": {
                "Name": "container_in_my_network",
                "EndpointID": "52cb1815755aedd0a9db3353b7fb9b55a6a5fb03563ac46e0bb03066455d4edd",
                "MacAddress": "02:42:ac:12:00:02",
                "IPv4Address": "172.18.0.2/16",
                "IPv6Address": ""

  ```
  
 `--driver` it's not necessary in this case becasue `bridge` is the default value but it must be used to create `overlay`, `macvlan` or `ipvlan` networks.
 
 `
## Docker Compose

In this chapther will talk about `docker-compose`, if you followed so far you know how to build images, run containers from it and use volumes and networks for storage and communication.

In a real develoment environment modern applicaton are composed by different services and each one needs to be wrapped in a different container. That means the more your application grows the more the number of containers to be managed grows. It's not possible start/stop/build manually each contianer everytime if your application has more than 2/3 servies.

Docker compose help us to solve this issue, you can think to it as an orchestrator to manage containers.
With `docker-compose` you can build/run/stop/stop all the services belonging to your application in a single command.


### Let's dirty our hands with docker-compose

In `examples/compose` you'll find a dev environment composed by a backend flask app a mysql databse and a nginx proxy.
There's a README file with all the insturctions to load this env. Briefly, in your lab (`vagrant ssh`)

* cd `/vagrant/examples/compose`
* create a .env file with the below content
  ```
  DB_USER=root
  DB_PASSWORD=db-78n9n
  DB_NAME=example
  DB_HOST=db
  MYSQL_DATABASE=example 
  MYSQL_ROOT_PASSWORD=db-78n9n
  ```
* run `docker-compose up`
* load some data `sudo chmod u+x ./setup.sh && ./setup.sh`

If you take a look at `docker-compose.yaml in `/vagrant/`examples/compose` you'll notice 4 top level nodes:

* `version`: it defines which version of docker-compose.yaml we wanna use
* `services`: it defines which services will be part of our application (`backend`, `db`, `proxy`)
* `volumes`: it defines volumes you wanna attach to rout service containers
* `network`: it defines docker networks you wanna create

`services` are our containers application and for each ones we need to specify every infos in order to inform compose how to build, start, expose a port, attach a volume or connect to a network and so on. For each of previous actions you know does exist a docker command but this time instead we'll use yaml field, for example let's take a look at the `backend` service in our `docker-compose.yaml`

  ```yaml
    backend:
      build: backend
      restart: always
      volumes:
        - ./backend:/code
      env_file:
        - .env
      stdin_open: true
      tty: true
      ports:
        - 5000:5000
      networks:
        - backnet
        - frontnet
      depends_on:
       - db
  ```

  just using yaml we're inforning compose that
  * `build`: build context resides in `backend` dir (if you rerember we used to define build context as last parameter in build cmd `docker build -t my_container backend`
  * `volumes`: attach `backend` dir as volume in `/code` dir in the container fs
  * `ports`: expose container port 5000 to the corresponding host one (`-p 5000:5000` in `docker run` cmd)
  * `networks`: connect `backend` container to both back and front networks
  * `depends_on`: do not start backend container before db

As you can see with compose you don't need to run any commands but you can obtain the same result with a yaml declative way.
We can't explore every yaml field in `docker-compose.yaml` definitions, but you can check official doc [here](https://docs.docker.com/compose/compose-file/) as referecnes

### Docker-compose commands

Let's come back to our lab (`vagrant up` -> `vagrant ssh` -> `cd /vagrant/examples/compose`) and let's try to build all the services defined in `docker-compose.yaml` running:

* `docker-compose build`

With a single command you can build all images, cool. But you can decide to build only one (or more), for example only `backend` service image:

* `docker-compose build backend`

Probably this time building phase took just some seconds and that's why you already built `backend` images when  you ran `docker-compose build` and because of you didn't change anything in the dockerfile docker used its caching system. Remember that you can force docker to do not use cache and forcing a new build:

* `docker-compose build --no-cache`

You should see your built images running

  ```
  vagrant@docker101:/vagrant/examples/compose$ docker images|grep compose
  compose_proxy       latest        9a5dd9c6b7af   10 minutes ago   18MB
  compose_backend     latest        3743a91dd0f0   10 minutes ago   55.9MB
  ```
As you maybe already noticed `docker-compose` named your images following this rule: <dir where yaml resides>_<service name> (e.g. `compose_proxy`)
  
Our images are ready we can create containers. Let's do that running 
  
* `docker-comose up`
  
After that you'll see application container up and running
  
  ```
  vagrant@docker101:~$ docker ps -a
  CONTAINER ID   IMAGE             COMMAND                  CREATED              STATUS                        PORTS                    NAMES
  4835a3d38a8a   compose_proxy     "nginx -g 'daemon of…"   About a minute ago   Up About a minute             0.0.0.0:80->80/tcp       compose_proxy_1
  d478faae32f0   compose_backend   "/bin/sh -c 'flask r…"   About a minute ago   Up About a minute             0.0.0.0:5000->5000/tcp   compose_backend_1
  a3a776f3652e   phpmyadmin        "/docker-entrypoint.…"   About a minute ago   Up About a minute             0.0.0.0:8080->80/tcp     compose_phpmyadmin_1
  d9c79449156e   mysql:8.0.19      "docker-entrypoint.s…"   About a minute ago   Up About a minute (healthy)   3306/tcp, 33060/tcp      compose_db_1
  ```
  
And if you inspect logs of the `up` command (pasted below)

  ```
  vagrant@docker101:/vagrant/examples/compose$ docker-compose up
  Creating network "compose_backnet" with the default driver
  Creating network "compose_frontnet" with the default driver
  Creating compose_phpmyadmin_1 ... done
  Creating compose_db_1         ... done
  Creating compose_backend_1    ... done
  Creating compose_proxy_1      ... done
  Attaching to compose_db_1, compose_phpmyadmin_1, compose_backend_1, compose_proxy_1
  ```
  
it's easy to understand that `up` command also creates networks and volumes if they do not exist and attach/connect containers to those ones  
  
  ```
  vagrant@docker101:~$ docker network ls|grep compose
  5c2c89c64aa8   compose_backnet    bridge    local
  e6de492c9b87   compose_frontnet   bridge    local
  ```
  
  ```
  vagrant@docker101:~$ docker volume ls|grep compose
  local     compose_db-data
  ```

You can stop running services typing `CTRL-C` in your terminal or running
  
 * `docker-compose stop`
  
  ```
  vagrant@docker101:/vagrant/examples/compose$ docker-compose stop
  Stopping compose_proxy_1      ... done
  Stopping compose_backend_1    ... done
  Stopping compose_phpmyadmin_1 ... done
  Stopping compose_db_1         ... done
  ```
  
Take in consideration you've just stopped containers (not removed) they do still exist
  
  ```
  vagrant@docker101:/vagrant/examples/compose$ docker ps -a
  CONTAINER ID   IMAGE             COMMAND                  CREATED          STATUS                          PORTS     NAMES
  4835a3d38a8a   compose_proxy     "nginx -g 'daemon of…"   15 minutes ago   Exited (0) About a minute ago             compose_proxy_1
  d478faae32f0   compose_backend   "/bin/sh -c 'flask r…"   15 minutes ago   Exited (0) About a minute ago             compose_backend_1
  a3a776f3652e   phpmyadmin        "/docker-entrypoint.…"   15 minutes ago   Exited (0) About a minute ago             compose_phpmyadmin_1
  d9c79449156e   mysql:8.0.19      "docker-entrypoint.s…"   15 minutes ago   Exited (0) About a minute ago             compose_db_1
  ```
  
You can re-start all those with both
  * `docker-compose start`
  * `docker-compose up`
  
  ```
  vagrant@docker101:/vagrant/examples/compose$ docker-compose start
  Starting db         ... done
  Starting backend    ... done
  Starting phpmyadmin ... done
  Starting proxy      ... done
  ```
  
  ```
  vagrant@docker101:/vagrant/examples/compose$ docker ps
  CONTAINER ID   IMAGE             COMMAND                  CREATED          STATUS                    PORTS                    NAMES
  4835a3d38a8a   compose_proxy     "nginx -g 'daemon of…"   17 minutes ago   Up 20 seconds             0.0.0.0:80->80/tcp       compose_proxy_1
  d478faae32f0   compose_backend   "/bin/sh -c 'flask r…"   17 minutes ago   Up 21 seconds             0.0.0.0:5000->5000/tcp   compose_backend_1
  a3a776f3652e   phpmyadmin        "/docker-entrypoint.…"   17 minutes ago   Up 21 seconds             0.0.0.0:8080->80/tcp     compose_phpmyadmin_1
  d9c79449156e   mysql:8.0.19      "docker-entrypoint.s…"   17 minutes ago   Up 21 seconds (healthy)   3306/tcp, 33060/tcp      compose_db_1
  ```
  
If you used `docker-compose start` as I did you lost logs (`docker-compse up` always attaches to pid 1 of its containers, you can avoid that running it in detaching mode: `docker-compose up -d`).
  
To see all logs just run:
  
  * `docker-compose logs`

Or for a specific service (e.g. `backend`)
  
  * `docker-compose logs backend`
  
If you wanna follow (in real-time) logs just use `-f` option
  
  * `docker-compose logs -f`, `docker-compse logs -f backend`
  
Finally if you want to destroy all services you can run:
  
  * `docker-compose down`
  
Be careful, it deletes not only containers but networks too
  
  ```
  vagrant@docker101:/vagrant/examples/compose$ docker-compose down
  Stopping compose_proxy_1      ... done
  Stopping compose_backend_1    ... done
  Stopping compose_phpmyadmin_1 ... done
  Stopping compose_db_1         ... done
  Removing compose_proxy_1      ... done
  Removing compose_backend_1    ... done
  Removing compose_phpmyadmin_1 ... done
  Removing compose_db_1         ... done
  Removing network compose_backnet
  Removing network compose_frontnet
  ```

but not associated volumes and images, you need to explicitly ask compse for that with options
  * `--rmi all`
  *  `-v`

For any doubts about a `<command>` just use `docker-compse <command> --help` (e.g. `docker-compse down --help`)
