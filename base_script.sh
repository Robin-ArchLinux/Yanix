#!/usr/bin/env bash

RED='\033[0;91m'
GREEN='\033[0;92m'
BLUE='\033[0;96m'
WHITE='\033[0;97m'
NC='\033[0m'

function logi() {
	local MSG="$1"
	echo -e "${GREEN}${MSG}${NC}"
}

function loge() {
	local MSG="$1"
	echo -e "${RED}error: ${MSG}${NC}"
	exit 1
}

function print_step() {
	STEP="$1"
	echo ""
	echo -e "${BLUE}# ${STEP} step${NC}"
	echo ""
}

function step() {
	local STEP="$1"
	eval "$STEP"
}

function pkg_install() {
  if pacman -Qi "$1" &>/dev/null; then
    logi "The package $1 is already installed"
  else
    logi "➜  pacman -S --noconfirm --needed $1"
    sudo pacman -S --noconfirm --needed "$1"
  fi
}