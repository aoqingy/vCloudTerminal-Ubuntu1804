#!/bin/bash
cd `dirname $0`
. ./vf_display.sh

pulseaudio -D


usbfilter='-1,-1,-1,-1,0'

cat > /tmp/vdi.vv << EOF
[virt-viewer]
type=spice
host=$1
port=$2
password=$3
tls-port=$4
fullscreen=1
title=$5
enable-smartcard=0
enable-usb-autoshare=1
delete-this-file=1
usb-filter=${usbfilter}
tls-ciphers=DEFAULT
host-subject=$6
ca=$7
toggle-fullscreen=shift+f11
release-cursor=shift+f12
secure-attention=ctrl+alt+end
secure-channels=main;inputs;cursor;playback;record;display;usbredir;smartcard
EOF


/usr/bin/remote-viewer --kiosk --kiosk-quit=on-disconnect --spice-usbredir-auto-redirect-filter=${usbfilter} --spice-usbredir-redirect-on-connect=${usbfilter} /tmp/vdi.vv
