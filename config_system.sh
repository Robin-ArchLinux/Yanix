#!/usr/bin/env bash
set -eu

source base_script.sh

function install_paru() {
  pkg_install "base-devel"
  git clone https://aur.archlinux.org/paru.git
  cd paru
  makepkg -si
}

function config_system() {
  logi "begin config system"
}