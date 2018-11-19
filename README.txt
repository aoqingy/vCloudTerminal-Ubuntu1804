vCloudTerminal-Ubuntu1804

sudo vim /etc/gdm3/custom.conf
Under [security] type AllowRoot=true so that it looks like
[security]
AllowRoot=true
Save and exit. Then run

sudo vim /etc/pam.d/gdm-password
Within this file you have comment out the line containing
auth required pam_succeed_if.so user != root quiet_success
so that it looks like this
#auth required pam_succeed_if.so user != root quiet_success



