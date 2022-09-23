import common_cmd

def install_basic_libs():
    # editor:
    common_cmd.aur_install("vim emacs code-git")
    #

def install_fonts():
    common_cmd.pac_install("noto-fonts noto-fonts-cjk  noto-fonts-emoji")

def install_fcitx():
    common_cmd.pac_install("fcitx fcitx-configtool fcitx-im")
    common_cmd.aur_install("fcitx-sogoupinyin")

def run():
    common_cmd.pac_install("gimp")
    # common_cmd.install_paru()
    # install_fonts()
    # install_fcitx()
    pass

