********************************
*
* Deployment Steps
*
********************************
1. Copy serhook.py to Hosts under /usr/libexec/vdsm/hooks/before_vm_start/


2. Identify the IP address of Cloud Terminal


3. Identify the virtual machine name of Cloud Desktop


4. Create ########.txt on Hosts under /usr/share/ovirt-engine/
192.168.0.232:12340
192.168.0.232:12341


********************************
*
* Runtime Steps
*
********************************
1. Power on Cloud Terminal

The following commands are executed with firefox on boot:
ser2net -C 12340:raw:0:/dev/ttyS0
ser2net -C 12341:raw:0:/dev/ttyS1


2. Start Cloud Desktop


********************************
*
* Verify Steps
*
********************************
minicom -c COM1 -H -w "1B5B2F31"
minicom -c COM1 -H -w "1B5B2F32"


********************************
*
* Issues
*
********************************
Problem: Serial Port is Used by Printer

Solution: In Control Panel - Management Tools - Print Manager, Select Customize Filter - All Drivers, Remove Object Driver, and then Restart Windows.
