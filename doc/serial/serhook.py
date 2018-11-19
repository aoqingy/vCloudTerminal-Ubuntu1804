#!/usr/bin/python
"""
Tweak an interface defintion so that its source is forced to be a specified
network. Applied on a per vnic basis, it gets triggered and used by two
different events:
    * before_device_create
    * before_nic_hotplug

This hook can be used to force a VM to use a libvirt network that is managed
outside of ovirt, such as an openvswitch network, or libvirt's default network.
"""


import os
import re
import sys
import json
import hooking
import traceback
import xml.dom

def addQemuNs(domXML):
    domain = domXML.getElementsByTagName('domain')[0]
    domain.setAttribute('xmlns:qemu',
                        'http://libvirt.org/schemas/domain/qemu/1.0')


def injectQemuCmdLine(domXML, qc):
    domain = domXML.getElementsByTagName('domain')[0]
    qctag = domXML.createElement('qemu:commandline')

    for cmd in qc:
        qatag = domXML.createElement('qemu:arg')
        qatag.setAttribute('value', cmd)
        qctag.appendChild(qatag)

    domain.appendChild(qctag)


def check_ip(ip):
    if re.match(r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$', ip):
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        domxml = hooking.read_domxml()

        deskname = domxml.getElementsByTagName('name')[0].firstChild.nodeValue
        hookfile = '/usr/share/ovirt-engine/%s.txt' % deskname
        params = ''
        if os.path.exists(hookfile):
            with open(hookfile, 'r') as stream:
                count = 0
                for line in stream.readlines():
                    try:
                        ip   = line.strip().split(':')[0].strip()
                        port = line.strip().split(':')[1].strip()
                        if not check_ip(ip):
                            raise Exception('IP invalid!')
                        if not int(port) in range(1024, 65536):
                            raise Exception('Port incorrect!')
                        if params == '':
                            params += '['
                        else:
                            params += ', '
                        params += '"-device", '
                        params += '"isa-serial,chardev=serial%s", ' % str(count)
                        params += '"-chardev", '
                        params += '"socket,id=serial%s,host=%s,port=%s"' % (str(count), ip, port)
                        count += 1
                    except Exception, e2:
                        pass
                if params:
                    params += ']'

        if params:
            addQemuNs(domxml)
            injectQemuCmdLine(domxml, json.loads(params))
            hooking.write_domxml(domxml)
    except:
        sys.stderr.write('qemu_cmdline: [unexpected error]: %s\n' % traceback.format_exc())
        sys.exit(2)
