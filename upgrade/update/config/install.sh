#!/bin/bash
cd `dirname $0`

echo
echo "Start to install config..."
echo

IsoVersion=`ls ../vfd/*.deb`
IsoVersion=${IsoVersion##*_}
IsoVersion=${IsoVersion//.deb}
ProductName="vCloudTerminal"

#Removed for EFI GRUB
#echo "Generating /etc/issue..."
#cat > ./etc/issue << EOF
#${ProductName} ${IsoVersion} \n \l
#EOF

#echo "Genertating /etc/issue.net..."
#cat > ./etc/issue.net << EOF
#${ProductName} ${IsoVersion}
#EOF

#echo "Generating /etc/lsb-release..."
#cat > ./etc/lsb-release << EOF
#DISTRIB_ID=${ProductName}
#DISTRIB_RELEASE=${IsoVersion%.*}
#DISTRIB_CODENAME=trusty
#DISTRIB_DESCRIPTION="${ProductName} ${IsoVersion}"
#EOF

#echo "Generting /etc/os-release..."
#cat > ./etc/os-release << EOF
#NAME="${ProductName}"
#VERSION="${IsoVersion}"
#ID=vClassTerminal
#ID_LIKE=debian
#PRETTY_NAME="${ProductName} ${IsoVersion}"
#VERSION_ID="${IsoVersion%.*}"
#HOME_URL="http://www.virtfan.com/"
#SUPPORT_URL="http://support.virtfan.com/"
#BUG_REPORT_URL="http://support.virtfan.com/"
#EOF

echo "Overwritting /etc..."
#复制编译环境中的用户配置
cp -a ./root/.profile /root/.profile
cp -a ./root/.config /root/.config       #禁止锁屏等因此而生效？(aoqingy)

#为IDV桌面桥接准备脚本
cp -a ./etc/qemu-ifup /etc/qemu-ifup
cp -a ./etc/qemu-ifdown /etc/qemu-ifdown
chmod +x /etc/qemu-ifup
chmod +x /etc/qemu-ifdown

#准备root用户自动登录
cp -a ./etc/pam.d/gdm-password /etc/pam.d/gdm-password
cp -a ./etc/pam.d/gdm-autologin /etc/pam.d/gdm-autologin
cp -a ./etc/gdm3/custom.conf /etc/gdm3/custom.conf

#运行虚拟机映像
mkdir -p /usr/sbin/virtfan
cp -a ./etc/rc.local /etc/rc.local
chmod +x /etc/rc.local        #必须将/etc/rc.local设为可执行文件，否则报错(aoqingy)

#执行定时调度任务
cp -a ./etc/crontab /etc/crontab

#GRUB
cp -a ./etc/default/grub /etc/default/grub

#禁用图像环境下快捷按键
cp -a ./etc/X11/xorg.conf /etc/X11/xorg.conf

#以下自动运行脚本根据当前语言更新公共路径名
#rm -r /etc/xdg/autostart/user-dirs-update-gtk.desktop	#为什么原来要删掉这个文件，留着行不行(aoqingy)

cp -a ./applications/* /usr/share/applications/    #在18.04环境下是否需要？(aoqingy)

#只能把关闭屏幕锁定放到编译环境准备中做，因为其运行需要DISPLAY(aoqingy)
#gsettings set org.gnome.desktop.session idle-delay 0
#gsettings set org.gnome.desktop.lockdown disable-lock-screen true

echo "Finish config installation."

