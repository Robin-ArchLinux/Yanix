#!/usr/bin/env bash
# shellcheck disable=SC1090
# SC1090: Can't follow non-constant source. Use a directive to specify location.

# -e参数表示只要shell脚本中发生错误，即命令返回值不等于0，则停止执行并退出shell
# -u参数表示shell脚本执行时如果遇到不存在的变量会报错并停止执行
set -eu

