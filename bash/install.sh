#!/usr/bin/env bash
# shellcheck disable=SC1090
# SC1090: Can't follow non-constant source. Use a directive to specify location.

# -e参数表示只要shell脚本中发生错误，即命令返回值不等于0，则停止执行并退出shell
# -u参数表示shell脚本执行时如果遇到不存在的变量会报错并停止执行
set -eu

CONFIG_FILE="yanix.conf"
VAR_FILE="vars.conf"
COMMON_SCRIPT="common.sh"

function welcome() {
	echo -e "Welcome Use This ArchLinux Install Script."
}

function init_config() {
	source $CONFIG_FILE
	source $COMMON_SCRIPT
}

function init_vars() {
	print_step "init_vars()"

	source $VAR_FILE
}

function configure_keymap() {
	if [ "$IS_DEBUG" == "true" ]; then
		info "in debug mode, skip config console keyboard map"
	else
		loadkeys "$KEYMAP"
		info "set console keymap to ${KEYMAP}"
	fi
}

function configure_time() {
	timedatectl set-ntp true
	set_timezone "${TIME_ZONE}"
}

function configure_reflector() {
	if [ "$REFLECTOR" == "false" ]; then
		if systemctl is-active --quiet reflector.service; then
			systemctl stop reflector.service
		fi
	fi
}

function partition () {
	echo "yes" | parted "${TARGET_DISK}" mklabel gpt
}


function prepare_install() {
	print_step "prepare_install()"

	configure_keymap
	configure_time
	configure_network
	configure_reflector
	partition
}

function install_system() {
	welcome
	init_config
	init_vars

	step "prepare_install"
}

function main() {
	install_system
}

main
