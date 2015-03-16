#!/bin/bash
cd /home/infoxel/tvkiller/server/media/sources
wget ftp://infoxel:123456@192.168.1.112/*.wmv -c --tries=1
#    rsync -av tvkiller@192.168.1.112:/cygdrive/c/Users/infoxel/Documents/VideosMarge/*.wmv /var/www/multimedia/ar/tvkiller/videos/ --append --recursive -e "sshpass -p pepito ssh"
#    sleep 1
