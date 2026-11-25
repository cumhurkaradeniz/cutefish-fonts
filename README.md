# Cutefish Fonts

A lightweight, macOS Font Book-inspired **Font Manager & Open-Source Font Catalog** for Linux with automatic OS language and Light/Dark theme support.

## Features
- **Live Font Preview:** Real-time preview of both installed system fonts and 115+ open-source Google Fonts before installation, with custom text and dynamic size slider (`12pt–72pt`).
- **One-Click Download & Install:** Download and install open-source fonts directly to `~/.local/share/fonts` with a single click.
- **Drag & Drop / Local Install:** Install `.ttf`, `.otf`, and `.ttc` files via file picker or drag-and-drop.
- **Safe Removal & Cache Refresh:** Safely remove user-installed fonts and rebuild the system font cache (`fc-cache -f`).
- **Multilingual:** Automatically adapts to OS language (`TR`, `EN`, `DE`, `FR`, `ES`, `RU`, `AR`).

## Installation

### Option 1: Debian / Ubuntu / CutefishOS (`.deb` Package)
```bash
sudo apt install ./cutefish-fonts_1.0.0_all.deb
```

### Option 2: Universal Linux Installer
```bash
git clone https://github.com
cd cutefish-fonts
bash install.sh
```
