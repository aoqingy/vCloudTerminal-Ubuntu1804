#!/bin/bash

#设置Citrix应用程序关联
dpkg -i /home/vCloudTerminal-Ubuntu1804/upgrade/update/10_deplist/deb.special/icaclient*.deb
dpkg -i /home/vCloudTerminal-Ubuntu1804/upgrade/update/10_deplist/deb.special/ctxusb*.deb		#这个包依赖于icaclient包，故放在后面
touch /tmp/empty.ica
firefox file:///tmp/empty.ica


reboot
