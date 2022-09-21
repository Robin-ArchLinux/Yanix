import common_cmd


def run():
    common_cmd.set_keyboard_layout("us")
    common_cmd.set_time_zone("Asia/Shanghai")
    home_file_list = common_cmd.list_dir("/home/robin")
