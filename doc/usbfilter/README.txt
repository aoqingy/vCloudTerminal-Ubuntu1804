#root@demo:/root# lsusb
#Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
#Bus 001 Device 004: ID 046d:c534 Logitech, Inc. Unifying Receiver
#Bus 001 Device 002: ID 0781:5567 SanDisk Corp. Cruzer Blade
#Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub

#0x046d=1133
#0xc534=50484

#The first matching rule applies

usbfilter='-1,1133,50484,-1,0|-1,-1,-1,-1,1'

/var/www/vfd/script/connect_via_idv.sh
/var/www/vfd/script/connect_via_spice.sh
