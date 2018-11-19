#!/bin/bash
cd `dirname $0`
. ./vf_display.sh


#while :
#do
#    rv=`ps -ef | grep "[q]emu-system-x86_64 .*-spice port=%s"` % $2
#    if ! test -z $rv; then
#        break
#    fi
#    sleep 1
#done


pulseaudio -D


usbfilter='-1,-1,-1,-1,0'

cat > /tmp/idv.vv << EOF
[virt-viewer]
type=spice
host=127.0.0.1
port=$2
fullscreen=1
title=$1
enable-smartcard=0
enable-usb-autoshare=1
delete-this-file=1
usb-filter=${usbfilter}
toggle-fullscreen=shift+f11
release-cursor=shift+f12
EOF


/usr/bin/remote-viewer --kiosk --kiosk-quit=on-disconnect --spice-usbredir-auto-redirect-filter=${usbfilter} --spice-usbredir-redirect-on-connect=${usbfilter} /tmp/idv.vv
