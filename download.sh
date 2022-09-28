#!/usr/bin/env bash
set -eu

YANIX_HTTPS_ADDRESS="https://github.com/Robin-ArchLinux/Yanix.git"
TMP_DIR="${HOME}/tmp"

function clone_and_run() {
  sudo pacman -S --noconfirm --needed git

  [ ! -d "$TMP_DIR" ] && mkdir "$TMP_DIR"
  local yanix_dir="${TMP_DIR}/Yanix"
  [ -d "$yanix_dir" ] && rm -rf "$yanix_dir"
  git clone $YANIX_HTTPS_ADDRESS "${TMP_DIR}/Yanix"
  cd "${TMP_DIR}/Yanix"
  # shellcheck disable=SC1090
  source "${1}.sh"
  ${1}
}


function main() {
  for arg in "$@"; do

    case $arg in

    -h | --help)
      usage
      exit 0
      ;;

    --install)
      clone_and_run --install
      ;;

    --config)
      clone_and_run config_system
      ;;

    esac
  done
}

main "$@"

