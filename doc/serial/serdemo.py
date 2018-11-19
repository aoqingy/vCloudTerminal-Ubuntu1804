#!/usr/bin/python
#-*-coding:utf-8 -*-
#apt-get install python-serial
#dmesg | grep ttyS0

#ser2net -C 12340:raw:0:/dev/ttyS0
#ser2net -C 12341:raw:0:/dev/ttyS1

import serial


#配置串口参数
ser = serial.Serial("/dev/ttyS0", baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=None)
print ser.name
print ser.baudrate
print ser.bytesize
print ser.parity
print ser.stopbits

#请输入密码
n = ser.write("\x1B\x5B\x2F\x31")
password1 = []
while True:
    if ser.inWaiting():
        try:
            n = ser.read(1)
            if ord(n) == 0x0d:
                break
            print ord(n)
            password1.append(ord(n))
        except Exception, e:
            print str(e)
print "Password: " + str(password1)

#请再输入一遍
n = ser.write("\x1B\x5B\x2F\x32")
password2 = []
while True:
    if ser.inWaiting():
        try:
            n = ser.read(1)
            if ord(n) == 0x0d:
                break
            print ord(n)
            password2.append(ord(n))
        except Exception, e:
            print str(e)
print "Password again: " + str(password2)

#关闭串口
n = ser.write("\x1B\x5B\x2F\x33")
ser.close()

#校验密码
if password1 == password2:
    print "Your password: " + str(password1)
else:
    print "Your password is not accepted!"
