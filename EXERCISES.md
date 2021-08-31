For a new emerging chinese client `dlopbox` you and your teammates have to implement a demo of a file sharing/syncronization software.
For the beta release there will be a master device and slaves ones. Documents inside dir under control in master device filesystem
must be syncronized in real time with all the slaves devices.

Architecture will be composed at least by:

* `master` where target dir resides
* `nginx` to serve static file inside dir under control in master device
* `inotify` deamon to monitor in real time filesystem events happening in the target dir of master device
* `flask` interface to collect events from `inotify` deamon. These events will be queued in `rabbit`.
* `rabbit` as queue system for collecting filesystem events
* `client` a software running in all the slave devices being able to connect to `rabbit` then dequeue events and download corresponding file from `nginx`

Other architecture constrains are:

* You must use `docker` or `docker-compose` for dev env
* `master` and `nginx` must share with each others the target dir through a `volume`
* `nginx` must serve all files in that volume
* `rabbit` needs too its own volume for persisting storage

