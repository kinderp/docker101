For a new emerging chinese client `dlopbox` you and your teammates have to implement a demo of a file sharing/syncronization software.
For the beta release there will be a master device and slaves ones. Documents inside dir under control in master device filesystem
must be syncronized in real time with all the slaves devices.

Architecture will be composed by the followting services:

* `master` where target dir resides
* `nginx` to serve static files inside dir under control in master device
* `inotify` deamon to monitor in real time filesystem events happening in the target dir of master device
* `flask` interface to collect events from `inotify` deamon. These events will be queued in `rabbit`
* `rabbit` as queue system for collecting filesystem events
* `client` a software running in all the slave devices being able to connect to `rabbit` then dequeue events and download corresponding file from `nginx`
* `mongo` as log system in order to store all events

Other architecture constrains are:

* You must use `docker` or `docker-compose` for dev env
* `master` and `nginx` must share with each others the target dir through a `volume`
* `nginx` must serve all files in that volume
* `rabbit` and `mongo` need too their own volumes for persisting storage

```
An   inotify    deemon
is running  on  master
It will trigger a call
to  service  interface 
at  every new fs event
occuring  i n  /shared 
+--------+
| MASTER |----+                                                                +-------+
+--------+    |                                             +----------------->| MONGO |
              |                                             |                  +-------+
              | /shared         ./mydocuments               |
        +------------+          +------+              +-----+-----+            +--------+           +-------+
        |   VOLUME   |----------| HOST !              | INTERFACE |----------->| RABBIT |<----------| CLIENT|
        +------------+          +------+              +-----------+            +--------+           +---+---+
              | /www/data                            (flask on 5000)                                    |
              |                                      It will queue  event                               |
              |                                      triggered by inotify                               |
+-------+     |                                      deamon on master                                   |
| NGINX |-----+                                                                                         |
+---+---+                                                                                               |
    |                                                                                                   |
    +---------------------------------------------------------------------------------------------------+
```

In `/vagrant/exercises/` you can find a dir for each of this services with code and Dockerfile(s).
A `docker-compose.yaml` is present in that dir too. You can test the whole system in this way:

* `vagrant ssh`
* `cd /vagrant/exercises`
* `docker-compose up -d`
* Get a shell in `client` container: `docker exec -it $(docker ps | grep myclient | awk '{ print $1 }') bash` 
* Do the same in master: `docker exec -it $(docker ps | grep mydropbox | awk '{ print $1 }') bash`
* Once inside `mydropbpx` container (above command), create a new file in `/shared`: `cd /shared && touch prova`
* In `client` container you should see the same file running `ls`

Reproduce the same architecture without `docker-compose` just using `docker` cli commands, in particular you have to:

* Build a container for each dir in `/vagrant/exercises/` (each dir corresponds to a service in `doccker-compose.yaml`)
* Create a dedicated network, each container will be placed in that network
* Crete volumes for `master`, `nginx`, `mongo` and `rabbit`. Remember `master` and `nginx` have to share the same dir (our target dir)
* Run manually each container with the correct options and reproduce all the test steps descrived above 
