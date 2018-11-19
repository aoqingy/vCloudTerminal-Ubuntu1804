#!/bin/bash

#root自动登录
sed -i 's/^mesg n .*/tty -s \&\& mesg n/g' /root/.profile
sed -i 's/auth\trequired\tpam_succeed_if.so user != root quiet_success/#auth\trequired\tpam_succeed_if.so user != root quiet_success/g' /etc/pam.d/gdm-password
sed -i 's/auth\trequired\tpam_succeed_if.so user != root quiet_success/#auth\trequired\tpam_succeed_if.so user != root quiet_success/g' /etc/pam.d/gdm-autologin
sed -i 's/#  AutomaticLoginEnable = true/AutomaticLoginEnable = true/g' /etc/gdm3/custom.conf
sed -i 's/#  AutomaticLogin = user1/AutomaticLogin = root/g' /etc/gdm3/custom.conf


reboot
