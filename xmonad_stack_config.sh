#!/usr/bin/env bash
set -eu

git submodule add https://github.com/xmonad/xmonad
git submodule add https://github.com/xmonad/xmonad-contrib

＃安装Stack
curl -sSL https://get.haskellstack.org/ | sh

# 初始化stack工程
stack init
# 编译安装包
stack install
# 将~/.local/bin目录添加到$PATH
# 注意: \$可以将字符串原汁原味的加入到文件，防止shell将变量转变为具体值.
printf "export PATH=\$HOME/.local/bin:\$PATH" >> $HOME/.zshrc
# printf "export PATH=/home/robin/.local/bin:\$PATH" >> /home/robin/.zshrc
