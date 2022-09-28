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

function install_common_software() {
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
    install_common_software
    install_fonts
}
