#!/bin/bash

#设置root密码
echo -e "123456\n123456" | sudo passwd

su
dhclient

#更新系统
rm /var/lib/dpkg/lock
apt-get update
apt-get dist-upgrade

#检出源代码
apt-get -y install git

cd /home
git clone ssh://aoqingyun@192.168.0.249:29418/virtclass/vCloudTerminal-Ubuntu1804.git


reboot
