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
