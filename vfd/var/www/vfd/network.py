#!/usr/bin/python
#-*-coding:utf-8 -*-
from flask import request
#from flask.ext.babel import gettext as _
import re
import os
import json
import time
import subprocess
from const   import *
from virtapi import *
from utility import *

#app = Flask(__name__)


##########################################################
#
# Network Related Logic
#
##########################################################
#@app.route('/api/network/get', methods=['GET'])
def get_network():
    logger.info("Entering get_network...")
    try:
        iptype, ipaddr, netmask, gateway, dns1, dns2 = get_ip_config()
        rv = {'iptype':iptype, 'ipaddr':ipaddr, 'netmask':netmask, 'gateway':gateway, 'dns1':dns1, 'dns2':dns2}

        logger.info(rv)
        return json.dumps({'code':'True', 'message':rv})
    except Exception, e:
        logger.error(str(e))
        return json.dumps({'code':'False', 'message':str(e)})


#@app.route('/api/network/set', methods=['POST'])
def set_network():
    logger.info('Enter set_network ...')
    try:
        iptype   = request.form.get('iptype',  '')
        ipaddr   = request.form.get('ipaddr',  '')
        netmask  = request.form.get('netmask', '')
        gateway  = request.form.get('gateway', '')
        dns1     = request.form.get('dns1',    '')
        dns2     = request.form.get('dns2',    '')

        logger.info('iptype:%s, ipaddr:%s, netmask:%s, gateway:%s, dns1:%s, dns2:%s' % (iptype, ipaddr, netmask, gateway, dns1, dns2))

        if iptype != 'static' and iptype != 'dhcp':
            raise Exception('Invalid Network Type!')
        if iptype == 'static':
            if ipaddr == '' or not check_ip(ipaddr):
                raise Exception('Invalid IP Address!')
            if netmask == '' or not check_netmask(netmask):
                raise Exception('Invalid Netmask!')
            if gateway and not check_ip(gateway):
                raise Exception('Invalid Gateway!')
        if dns1 and not check_ip(dns1):
            raise Exception('Invalid DNS Address!')
        if dns2 and not check_ip(dns2):
            raise Exception('Invalid DNS Address!')

        set_ip_config(iptype, ipaddr, netmask, gateway, dns1, dns2)

        logger.info('Done!')
        return json.dumps({'code':'True', 'message':'Done!'})
    except Exception, e:
        logger.error(str(e))
        return json.dumps({'code':'False', 'message':str(e)})


#@app.route('/api/network/restart', methods=['POST'])
def restart_network():
    logger.info("Entering restart_network...")
    try:
        iptype   = request.form.get('iptype',  '')
        ipaddr   = request.form.get('ipaddr',  '')
        netmask  = request.form.get('netmask', '')
        gateway  = request.form.get('gateway', '')
        dns1     = request.form.get('dns1',    '')
        dns2     = request.form.get('dns2',    '')

        logger.info('iptype:%s, ipaddr:%s, netmask:%s, gateway:%s, dns1:%s, dns2:%s' % (iptype, ipaddr, netmask, gateway, dns1, dns2))

        if iptype != 'dhcp' and iptype != 'static' and iptype != 'bridge/dhcp' and iptype != 'bridge/static':
            raise Exception('Invalid Network Type!')
        if iptype == 'static' or iptype == 'bridge/static':
            if ipaddr == '' or not check_ip(ipaddr):
                raise Exception('Invalid IP Address!')
            if netmask == '' or not check_netmask(netmask):
                raise Exception('Invalid Netmask!')
            if gateway and not check_ip(gateway):
                raise Exception('Invalid Gateway!')
        if dns1 and not check_ip(dns1):
            raise Exception('Invalid DNS Address!')
        if dns2 and not check_ip(dns2):
            raise Exception('Invalid DNS Address!')

        set_ip_config(iptype, ipaddr, netmask, gateway, dns1, dns2)

        logger.info('Done!')
        return json.dumps({'code':'True', 'message':'Done!'})
    except Exception, e:
        logger.error(str(e))
        return json.dumps({'code':'False', 'message':str(e)})


##########################################################
#
# Wifi Related Logic
#
##########################################################
#@app.route('/api/wifi/scan', methods=['POST'])
def scan_wifi():
    logger.info("Entering scan_wifi...")

    try:
        wic = check_wic()
        if not wic:
            raise Exception('Wifi nic not found!')

        wifi = []
        os.popen('rfkill unblock all')
        os.popen('ip link set %s up' % wic)
        for ln in os.popen("iwlist %s scan | grep ESSID" % wic, 'r'):
            wifi.append(re.search('ESSID:\"(?P<%s>.+)\"\s' % wic, ln).group(wic))

        rwifi = []
        for ls in sorted(list(set(wifi))):
            rwifi.append(ls.decode('string_escape'))

        return json.dumps({'code':'True', 'message':rwifi})
    except Exception, e:
        logger.error(str(e))
        return json.dumps({'code':'False', 'message':str(e)})


#@app.route('/api/wifi/status', methods=['GET'])
def status_wifi():
    logger.info("Entering status_wifi...")

    try:
        wic = check_wic()
        if not wic:
            raise Exception('Wifi nic not found!')

        rwifi = []
        for ln in os.popen("iwgetid %s" % wic, 'r'):
            try:            
                rwifi.append(re.search('ESSID:\"(?P<wifi>.+)\"\s', ln).group('wifi'))
            except Exception, e2:
                pass

        logger.info(rwifi)
        return json.dumps({'code':'True', 'message':rwifi})
    except Exception, e:
        logger.error(str(e))
        return json.dumps({'code':'False', 'message':str(e)})


#@app.route('/api/wifi/connect', methods=['POST'])
def connect_wifi():
    logger.info("Entering connect_wifi...")
    ssid     = request.form.get('ssid')
    password = request.form.get('password')
    logger.info('ssid: %s' % ssid)

    try:
        wic = check_wic()
        f = open('/etc/netplan/01-network-manager.yaml', 'w')
        f.write('\n')
        f.write('network:\n')
        f.write('  version: 2\n')
        f.write('  renderer: NetworkManager\n')
        f.write('  wifis:\n')
        f.write('    %s:\n' % wic)
        f.write('      access-points:\n')
        f.write('        "%s":\n' % ssid)
        f.write('          password: %s\n' % password)
        f.close()

        command = "netplan apply"
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        out, err = p.communicate()
        time.sleep(3)

        logger.info('Done!')
        return json.dumps({'code':'True', 'message':'Done!'})
    except Exception, e:
        logger.error(str(e))
        return json.dumps({'code':'False', 'message':str(e)})


#@app.route('/api/wifi/disconnect', methods=['POST'])
def disconnect_wifi():
    logger.info("Entering disconnect_wifi...")
    try:
        wic = check_wic()
        if not wic:
            raise Exception('Wifi nic not found!')

        command = 'ip link set %s down' % wic
        logger.info(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        out, err = p.communicate()     #调用此语句之后returncode才有效(aoqingy)
        if p.returncode != 0:
            raise Exception("Fail to disconnect wifi!")

        logger.info('Done!')
        return json.dumps({'code':'True', 'message':'Done!'})
    except Exception, e:
        logger.error(str(e))
        return json.dumps({'code':'False', 'message':str(e)})


##########################################################
#
# Network Test Related
#
##########################################################
#@app.route('/api/network/ping1', methods=['POST'])
def ping1():
    logger.info("Entering ping1...")
    ip = request.form.get('ip', '')
    logger.info("ip: %s" % ip)

    try:
        if not ip:
            raise Exception("IP address invalid!")

        pinfo = ''
        for ln in os.popen('ping %s -w 1 -c 1' % ip, 'r'):
            status = re.search('(?=PING).+', ln)
            if status:
                pinfo = status.group(0)
                break

        if pinfo == '':
            raise Exception('ping: unknown host ' + ip)

        logger.info(pinfo)
        return json.dumps({'code':'True', 'message':pinfo})
    except Exception, e:
        logger.error(str(e))
        return json.dumps({'code':'False', 'message':str(e)})


#@app.route('/api/network/ping2', methods=['POST'])
def ping2():
    logger.info("Entering ping2...")
    ip = request.form.get('ip', '')
    logger.info("ip: %s" % ip)

    try:
        if not ip:
            raise Exception('IP address invalid!')

        pinfo = ''
        for ln in os.popen('ping %s -w 1 -c 1' % ip, 'r'):
            status = re.search('.+(?=icmp_seq).+', ln)
            if status:
                pinfo = status.group(0)
                break

        if pinfo == '':
            raise Exception('1 packets transmitted, 0 received, 100% packet loss, time 0ms')

        logger.info(pinfo)
        return json.dumps({'code':'True', 'message':pinfo})
    except Exception, e:
        logger.error(str(e))
        return json.dumps({'code':'False', 'message':str(e)})

