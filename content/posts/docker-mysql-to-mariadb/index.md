---
author: Nathan Vaughn
cover: img/mysql_to_mariadb.jpg
userelativecover: true
date: "2019-07-20"
description: Replacing existing MySQL 8 containers in Docker Compose stacks with MariaDB
images:
  - /posts/docker-mysql-to-mariadb/img/mysql_to_mariadb.jpg
tags:
  - Docker
  - MySQL
  - MariaDB
  - bash
title: Converting MySQL 8 Docker Containers to MariaDB
---

## Background

Recently, when I setup a number of Docker Compose stacks for myself, I naively
used MySQL 8 databases. I had heard of MariaDB in the past, and knew it was a
drop-in replacement to MySQL, but I didn't really know much about it.
After recently reading about some of MariaDB's
[features and speed-improvements](https://mariadb.com/kb/en/library/mariadb-vs-mysql-features/)
over MySQL Community Edition
(and [many people](https://www.reddit.com/r/sysadmin/search/?q=flair_name%3A%22Rant%22%20oracle&restrict_sr=1)
including myself **_really_** hate Oracle),
I decided I wanted to swap out my MySQL databases.
This ended up being more complicated than I initially hoped.

## Challenge

The challenge was that I had previously used MySQL 8 for my databases.
This presented the problem that I simply couldn't stop the old MySQL container,
and start a new MariaDB container with the existing volume of the `/var/lib/mysql`
folder (which contains MySQL's data) as is supported
with [older versions of MySQL](https://mariadb.com/kb/en/library/upgrading-from-mysql-to-mariadb/).
This meant that I would need to export the data from each database, delete the volume,
start a new MariaDB database, and reimport the data. While it sounds simple enough,
it quickly became very tedious.

## Process

The general process was as follows:

- Dump the MySQL database of the current database container.

  `sudo docker exec -i container_name mysqldump -u username -p database > database_db.sql`

- Stop the Docker Compose stack.

  `sudo docker-compose down`

- Change the `docker-compose.yml` file to use MariaDB.

```diff
-   command: '--default-authentication-plugin=mysql_native_password'
        env_file:
            - ./.env
-   image: 'mysql:latest'
+   image: 'mariadb:latest'
```

- Delete the old data volume.

  `sudo docker volume rm volume_name`

- Start the modified Docker Compose stack.

  `sudo docker-compose up -d`

- Wait for the MariaDB container to become ready, and load in the data.

  `sudo docker exec -i container_name mysql -u username -p database < database_db.sql`

## Automating

After doing this process by hand twice, I quickly decided to write a script to do it
for me as I use a standard naming convention for all of my Docker Compose stacks and really
wanted to speed up the process

**_WARNING: DON'T USE THIS SCRIPT WITHOUT GOOD BACKUPS_**

```bash
#!/bin/bash

# inputs

echo "Enter application name (lower case):"
read APPNAME

read -p "Enter the directory with the docker-compose.yml file: " -e -i `pwd`/$APPNAME DOCKERDIR
read -p "Enter the container name: " -e -i ${APPNAME}_db_1 CONTAINERNAME
read -p "Enter the container volume name: " -e -i ${APPNAME}_db_data VOLUMENAME
read -p "Enter the MySQL database: " -e -i $APPNAME DATABASE
read -p "Enter the MySQL username: " -e -i $APPNAME USERNAME
read -p "Enter the MySQL password: " -s PASSWORD

# -----------------
# Data export

FILENAME=${DATABASE}_db.sql

echo "Changing directories to $DOCKERDIR"
cd $DOCKERDIR

echo "Dumping MySQL database to $FILENAME"
sudo docker exec -i $CONTAINERNAME mysqldump -u $USERNAME -p$PASSWORD $DATABASE > $FILENAME

echo "Stopping containers"
sudo docker-compose down

# -----------------
# Wait for user to modify compose file

read -p "Press enter once you have modified the docker-compose.yml file"

# -----------------
# Data import

echo "Changing directories to $DOCKERDIR"
cd $DOCKERDIR

echo "Deleting old volume $VOLUMENAME"
sudo docker volume rm $VOLUMENAME

echo "Starting containers"
sudo docker-compose up -d

echo "Waiting 90 seconds"
sleep 90

echo "Loading MySQL database from $FILENAME"
echo "sudo docker exec -i $CONTAINERNAME mysql -u $USERNAME -p$PASSWORD $DATABASE < $FILENAME"
sudo docker exec -i $CONTAINERNAME mysql -u $USERNAME -p$PASSWORD $DATABASE < $FILENAME

#echo "Removing $DOCKERDIR/$FILENAME"
#rm $DOCKERDIR/$FILENAME
```

## Conclusion

With a bit of time and effort, I've now converted all my MySQL databases to MariaDB
as part of my goal of [ridding myself](https://www.cnbc.com/2018/08/01/amazon-plans-to-move-off-oracle-software-by-early-2020.html) of all Oracle software.
