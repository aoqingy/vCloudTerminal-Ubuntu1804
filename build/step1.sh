#!/bin/bash

#配置网络
#printf "\nauto ens33\niface ens33 inet static\n    address 192.168.0.237\n    netmask 255.255.255.0\n    gateway 192.168.0.1\n\ndns-nameservers 192.168.0.1\n" >>/etc/network/interfaces
#systemctl restart networking
rm -rf /etc/netplan/*
printf "\nnetwork:\n  version: 2\n  renderer: networkd\n  ethernets:\n    ens33:\n      dhcp4: no\n      dhcp6: no\n      addresses: [192.168.0.237/24]\n      gateway4: 192.168.0.1\n      nameservers:\n        addresses: [192.168.0.1,8.8.8.8]" >>/etc/netplan/01-netcfg.yaml
#systemctl stop NetworkManager.service
#systemctl disable NetworkManager.service
systemctl restart systemd-networkd
systemctl enable systemd-networkd


#安装必需软件包
rm /var/lib/dpkg/lock
apt-get update
apt-get dist-upgrade
apt-get -y install vim ssh
apt-get -y install cython python-m2crypto    #编译py到so
apt-get -y autoremove
#apt-get -y install squashfs-tools compizconfig-settings-manager    #To Consider (aoqingy)

#配置SSH服务
sed -i -e 's/#PermitRootLogin .*/PermitRootLogin yes/g' /etc/ssh/sshd_config
systemctl enable ssh
systemctl restart ssh


reboot
