#!/bin/bash
cd `dirname $0`
. ./vf_display.sh

cat > /tmp/vnc.vv << EOF
[virt-viewer]
type=vnc
host=$1
port=$2
password=$3
delete-this-file=1
EOF

/usr/bin/remote-viewer --kiosk /tmp/vnc.vv
