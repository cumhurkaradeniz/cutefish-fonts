#!/bin/bash
set -e
mkdir -p pkg/DEBIAN pkg/usr/share/cutefish-fonts pkg/usr/share/applications pkg/usr/bin pkg/usr/share/icons/hicolor/256x256/apps
cp app.py font_mgr.py i18n.py icon.png pkg/usr/share/cutefish-fonts/
cp icon.png pkg/usr/share/icons/hicolor/256x256/apps/cutefish-fonts.png
cat << 'CTRL' > pkg/DEBIAN/control
Package: cutefish-fonts
Version: 1.0.0
Section: utils
Priority: optional
Architecture: all
Depends: python3, python3-pyqt5, fontconfig
Maintainer: Cumhur Karadeniz <cumhurkaradeniz@github.com>
Description: Modern macOS Font Book style Font Manager & Open-Source Font Catalog for Linux
CTRL
printf '#!/bin/bash\nexec python3 /usr/share/cutefish-fonts/app.py "$@"\n' > pkg/usr/bin/cutefish-fonts && chmod +x pkg/usr/bin/cutefish-fonts
cat << 'DSK' > pkg/usr/share/applications/cutefish-fonts.desktop
[Desktop Entry]
Name=Cutefish Fonts
Comment=Modern Font Manager & Open-Source Font Catalog for Linux
Exec=cutefish-fonts
Icon=cutefish-fonts
Terminal=false
Type=Application
Categories=Utility;Graphics;
StartupWMClass=cutefish-fonts
DSK
dpkg-deb --root-owner-group --build pkg cutefish-fonts_1.0.0_all.deb && rm -rf pkg
