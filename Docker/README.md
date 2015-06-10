Usage
===

 1/ Docker image download
---

```
[user@host~]$ sudo docker pull prodiguer/synda
```

2/ Host side directories setup and OpenID/Password configuration
---

```
[user@host~]$ mkdir -p ~/synda/sdt/conf; wget -O ~/synda/sdt/conf/sdt.conf https://github.com/Prodiguer/synda/raw/master/sdt/conf/sdt.conf
[user@host~]$ vi ~/synda/sdt/conf/sdt.conf
```

3/ Startup container in daemon mode and mount host directories as container data volumes owned by your host user and group
---

```
[user@host~]$ sudo docker run -d -t -i -v ~/synda/sdt/data/:/home/synda/sdt/data/ -v ~/synda/sdt/db/:/home/synda/sdt/db/ -v ~/synda/sdt/log/:/home/synda/sdt/log/ -v ~/synda/sdt/selection:/home/synda/sdt/selection/ -v ~/synda/sdt/conf/:/home/synda/sdt/conf/ -e UID=$UID -e GID=$GROUPS prodiguer/synda /bin/bash
```

4/ Dataset installation and download
---

```
[user@host~]$ sudo docker ps
[user@host~]$ sudo docker attach 204fcee0d7e5
[synda@204fcee0d7e5 ~]$ synda install [dataset_name]
[synda@204fcee0d7e5 ~]$ synda daemon start &
```

5/ Container detachment
---

```
[synda@204fcee0d7e5 ~]$ Ctrl+p+Ctrl+q
```

6/ Listing retrieved data, logs, db, selection and config on host directories
---

```
[user@host~]$ ls ~/synda/sdt/data/
[user@host~]$ ls ~/synda/sdt/log/
[user@host~]$ ls ~/synda/sdt/db/
[user@host~]$ ls ~/synda/sdt/selection/
[user@host~]$ ls ~/synda/sdt/conf/
```
