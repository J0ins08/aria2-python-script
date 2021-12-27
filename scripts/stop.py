# -*- encoding: utf-8 -*-
#@File      :   stop.py
#@Time      :   2021/12/23 16:21:37
#@Author    :   J0ins08
#@Software  :   Visual Studio Code

from aria2 import *

if __name__ == '__main__':
    remove_aria2_file()
    remove_download_file()
    remove_torrent_file()