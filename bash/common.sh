#!/usr/bin/env bash

<<<<<<< HEAD
RED='\033[0;91m'
GREEN='\033[0;92m'
BLUE='\033[0;96m'
WHITE='\033[0;97m'
NC='\033[0m'

function info() {
	local MSG="$1"
	echo -e "${GREEN}${MSG}${NC}"
}

function error() {
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
=======
source base_script.sh
>>>>>>> d0b4e78 (重构目录结构)

function pac_install() {
	local ERROR="true"
	local PACKAGES=()
	set +e
	IFS=' ' read -ra PACKAGES <<<"$1"
	for VARIABLE in {1..5}; do
		local COMMAND="pacman -Syu --noconfirm --needed ${PACKAGES[*]}"
		if execute_sudo "$COMMAND"; then
			local ERROR="false"
			break
		else
			sleep 10
		fi
	done
	set -e
	if [ "$ERROR" == "true" ]; then
		exit 1
	fi
}

function execute_sudo() {
	local COMMAND="$1"
	if [ "${var_on_install_process}" == "true" ]; then
		arch-chroot "${MNT_DIR}" bash -c "$COMMAND"
	else
		sudo bash -c "$COMMAND"
	fi
}

function configure_network() {
	if [ -n "$WIFI_INTERFACE" ]; then
		iwctl --passphrase "$WIFI_KEY" station "$WIFI_INTERFACE" connect "$WIFI_ESSID"
		sleep 10
	fi

	# only one ping -c 1, ping gets stuck if -c 5
	if ! ping -c 1 -i 2 -W 5 -w 30 "$PING_HOSTNAME"; then
		error "Network ping check failed. Cannot continue."
	fi
}

function set_timezone() {
	local time_zone="$1"
	timedatectl set-time_zone "$time_zone"
}
