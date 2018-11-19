#!/bin/bash
cd `dirname $0`

echo
echo "Start to install ngrok ..."
echo

echo "Installing ngrok..."
cp ./sunny.py /usr/sbin/sunny.py
chmod +x /usr/sbin/sunny.py

echo "Finish ngrok installation."

