# docker101

### Playground

We'll use vagrant in order to obtain a clean environment as lab where we'll be free to play with docker without any fear to break our dev env. 
So before doing anything you shuold:

* Install `virtualbox`
* Install `vagrant`

#### Start lab

1. Clone this repo
2. move to `ubuntu` dir
3. Run `vagrant up` and wait
5. Ssh into vm `vagrant ssh`
6. Check if docker has been provisioned correctly
   * `systemctl status docker`
   * `docker ps`



