# Installation

FocusDeck currently supports Linux distributions using the freedesktop desktop standard.

## Supported Distributions

- Fedora
- Ubuntu
- Linux Mint
- Debian
- Pop!_OS
- Arch Linux
- EndeavourOS
- Zorin OS


## Quick Install

```bash
curl -L https://raw.githubusercontent.com/sm4006/FOCUSDECK/main/install.sh -o install.sh
chmod +x install.sh
./install.sh
```

## What the installer does

The installer automatically:

- Downloads the latest FocusDeck release binary
- Creates a desktop launcher
- Installs the OLED application icon
- Registers FocusDeck with the application menu

---

## Installed Locations

| Component | Location |
|-----------|----------|
| Binary | ~/.local/share/focusdeck/ |
| Desktop Entry | ~/.local/share/applications/ |
| Icon | ~/.local/share/icons/hicolor/256x256/apps/ |

---

## Manual Launch

If required, FocusDeck can be started manually:

```bash
~/.local/share/focusdeck/FocusDeck
```

---

## Uninstall

```bash
rm -rf ~/.local/share/focusdeck
rm ~/.local/share/applications/focusdeck.desktop
rm ~/.local/share/icons/hicolor/256x256/apps/focusdeck.png
```