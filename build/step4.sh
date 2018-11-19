#!/bin/bash

#运行之以便生成/root/.mozilla目录
firefox

#禁用鼠标移动到顶部时浏览器退出全屏
for path in /root/.mozilla/firefox/*.default; do mkdir -p $path/chrome; done
for path in /root/.mozilla/firefox/*.default/chrome; do echo -e "@namespace url(\"http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul\");\n#fullscr-toggler { display:none!important; }" > $path/userChrome.css; done

#浏览器配置
for path in /root/.mozilla/firefox/*.default; do touch $path/user.js; done

./firefox_update.sh /root/.mozilla/firefox/*.default/user.js browser.startup.homepage localhost string
./firefox_update.sh /root/.mozilla/firefox/*.default/user.js privacy.history.custom true bool
./firefox_update.sh /root/.mozilla/firefox/*.default/user.js browser.privatebrowsing.autostart true bool
./firefox_update.sh /root/.mozilla/firefox/*.default/user.js places.history.enabled false bool
./firefox_update.sh /root/.mozilla/firefox/*.default/user.js browser.formfill.enable false bool
./firefox_update.sh /root/.mozilla/firefox/*.default/user.js signon.rememberSignons false bool
./firefox_update.sh /root/.mozilla/firefox/*.default/prefs.js app.update.auto false bool
./firefox_update.sh /root/.mozilla/firefox/*.default/prefs.js app.update.enabled false bool
./firefox_update.sh /root/.mozilla/firefox/*.default/prefs.js app.update.staging.enabled false bool
./firefox_update.sh /root/.mozilla/firefox/*.default/prefs.js extensions.update.autoUpdateDefault false bool
#./firefox_update.sh /root/.mozilla/firefox/*.default/prefs.js extensions.update.enabled false bool


reboot
