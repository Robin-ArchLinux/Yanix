#!/usr/bin/env bash
set -eu

source base_script.sh

function install_paru() {
  logi "begin install paru"
  if has_installed "paru"; then
    logi "paru has installed"
  else
    pkg_install "base-devel"
    git clone https://aur.archlinux.org/paru.git
    cd paru
    makepkg -si
  fi
}

function install_common_pkg() {
  logi "install common software"
  local list=(
    firefox
    sublime-text-4
    meld
    telegram-desktop
    discord
    scrot
  )
  pkg_list_install "${list[@]}"
}

function install_fonts() {
  logi "install fonts"
}

function config_sound() {
  logi "config sound"
}

function config_samba() {
  logi "config samba"
}

function config_network_discovery() {
  logi "config network discovery"
}

function config_printers() {
  logi "config printers"
}

function config_system() {
  logi "begin config system"
  install_paru
  install_common_pkg
  install_fonts
}

echo "update system before do further operation."
sudo pacman --noconfirm -Syu

echo "install basic tooltip package"
sudo pacman -S --noconfirm --needed base-devel wget git

install_paru

install_fonts

sudo pacman -S --noconfirm --needed rofi feh xmonad xmonad-contrib xmobar xterm alacritty

mkdir -p ~/.config/xmonad && cd ~/.config/xmonad
