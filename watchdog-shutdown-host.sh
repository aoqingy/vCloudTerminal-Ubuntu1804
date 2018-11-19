#!/bin/bash
#-*-coding:utf-8 -*-

#判断是否有IDV或VDI桌面在运行，若有继续检测
uptime=`awk '{print int($1)}' /proc/uptime`	#以秒为单位
if [ $uptime -gt 300 ]; then
    while true
    do
        pgrep qemu-system-x86_64 || shutdown -d -f
	pgrep remote-viewer || shutdown -d -f
        sleep 1
    done
fi
