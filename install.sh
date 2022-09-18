#!/usr/bin/env bash
# shellcheck disable=SC1090,SC2034
# SC1090: Can't follow non-constant source. Use a directive to specify location.

# -e参数表示只要shell脚本中发生错误，即命令返回值不等于0，则停止执行并退出shell
# -u参数表示shell脚本执行时如果遇到不存在的变量会报错并停止执行
set -eu

function pac_install() {
	local ERROR="true"
	set +e

	local COMMAND="pacman -Syu --noconfirm --needed $*"

	local n=0
	local max_try=3
	until [ "$n" -ge $max_try ]; do
		if execute_sudo "$COMMAND"; then
			local ERROR="false"
			break
		else
			n=$((n + 1))
			if ((n < max_try)); then
				sleep_time=5
				echo "install failed, try again after ${sleep_time} seconds."
				sleep $sleep_time
			fi
		fi
	done

	set -e
	if [ "$ERROR" == "true" ]; then
		exit 1
	fi
}

function execute_sudo() {
	local COMMAND="$1"
	sudo bash -c "$COMMAND"
}

function usage() {
	echo "this is archlinux install and config script, use install args to install archlinux, use config to configure archlinux"
}

function install() {
	echo "install script should be written later"
}

function config_system() {
	pac_install git
	git clone 
}

function main() {
	for arg in "$@"; do

		case $arg in

		-h | --help)
			usage
			exit 0
			;;

		install) ;;

		config)
			config_system
			;;

		esac
	done
}

main "$@"
