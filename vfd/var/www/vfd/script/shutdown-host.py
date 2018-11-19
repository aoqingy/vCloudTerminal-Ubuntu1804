#!/bin/bash
#实现关机联动（也就是在关闭虚拟机时自动关闭云终端）
import time
#product  = request.form.get('product' , '')
#nickname = request.form.get('nickname', '')
#serverip = request.form.get('serverip', '')
#username = request.form.get('username', '')
#password = request.form.get('password', '')
#domain   = request.form.get('domain'  , '')

def getIDVStatus(vmname):
    return 'DOWN'

def getSpiceStatus(serverip, username, password, domain):
    return 'DOWN'

def getStatus(product, serverip, username, password, domain):
    if product == 'idv-desktop':
        status = getIDVStatus(vmname)
    elif product = 'spice-desktop':
        status = getSpiceStatus(serverip, username, password, domain):
    else:
        status = 'DOWN'


#首先监控确保虚拟机进入运行状态
while True:
    status = getStatus()
    if status == 'UP':
        break
    time.sleep(1)

#然后轮询等待虚拟机进入关机状态
while True:
    status = getStatus()
    if status == 'DOWN':
        break
    time.sleep(1)

shutdown -d -f -i
