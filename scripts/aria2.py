# -*- encoding: utf-8 -*-
#@File      :   aria2.py
#@Time      :   2021/12/23 16:11:05
#@Author    :   J0ins08
#@Software  :   Visual Studio Code

import re
from urllib import request, parse
import os
import datetime
import sys
import shutil
import json
import base64
import magneturi

def get_aria2_parameter(keyword):
    '''从aria2.conf中获取参数'''
    with open(aria2_config,'r',encoding='utf-8') as config:
        for line in config:
            if keyword in line:
                parammeter = re.search('=(.*)',line).group(1)
                return parammeter

def get_download_file():
    '''获取下载文件名'''
    if len(sys.argv) == 4:
        sys.exit()
    elif len(sys.argv) == 5:
        download_file = sys.argv[4]
    else:
        download_file = ' '.join(sys.argv[4:])
    return download_file

def get_infoHash(gid):
    '''通过RPC获取BT下载任务的infoHash'''
    payload = {
        'jsonrpc':'2.0',
        'id':'Alpha',
        'method':'aria2.tellStatus',
        'params':[f'token:{rpc_secret}', gid]}
    url = f'http://localhost:{rpc_listen_port}/jsonrpc'
    data = json.dumps(payload).encode('utf-8')
    response = request.urlopen(url=url, data=data)
    infoHash = dict(json.loads(response.read()))['result']['infoHash']
    return infoHash

def count_infoHash(torrent_file):
    '''计算种子的infoHash'''
    magnet_uri = magneturi.from_torrent_file(torrent_file)
    b32Hash = re.search('btih:(.{32})',magnet_uri).group(1)
    b16Hash = base64.b16encode(base64.b32decode(b32Hash))
    infoHash = b16Hash.decode('utf-8').lower()
    return infoHash

def get_file_folder():
    '''获取下载的文件夹'''
    file_folder = re.match(f'{download_path}/.*?/', 
                           download_file).group()[:-1]
    return file_folder

def get_aria2_file():
    '''获取后缀为.aria2的文件'''
    if download_path == os.path.dirname(download_file):
        aria2_file = download_file + '.aria2'
    else:
        aria2_file = get_file_folder() + '.aria2'
    return aria2_file

def remove_torrent_file():
    '''删除种子文件'''
    try:
        torrent_file = os.path.join(download_path,
                                    f'{get_infoHash(gid)}.torrent')
    except KeyError:
        print(f'{time} Task:{gid} is a HTTP/HTTPS download task, '
              'only BitTorrent task has infoHash.')
    else:
        if os.path.exists(torrent_file):
            os.remove(torrent_file)
        else:
            for file in os.listdir(download_path):
                if file.endswith('torrent'):
                    torrent_file= os.path.join(download_path,file)
                    infoHash = count_infoHash(torrent_file)
                    if infoHash == get_infoHash(gid):
                        os.remove(torrent_file)

def remove_aria2_file():
    '''删除后缀为.aria2文件'''
    os.remove(get_aria2_file())

def remove_download_file():
    '''删除下载文件或文件夹'''
    if download_path == os.path.dirname(download_file):
        os.remove(download_file)
    else:
        shutil.rmtree(get_file_folder())

def get_contents():
    '''获取推送消息内容'''
    if download_path == os.path.dirname(download_file):
        contents = (os.path.basename(download_file) + 
                    ' 下载完成。' + '\n' + time)
    else:
        contents = (os.path.split(get_file_folder())[1] + 
                    ' 下载完成。' + '\n' + time)
    return contents

def push2bark(contents):
    '''推送通知到Bark客户端'''
    url = 'https://api.day.app/push'
    headers={"Content-Type": "application/json; charset=UTF-8"}
    data = {
        "title": 'Aria2',
        "body": contents,
        "device_key": '',
        "ext_params": {
            "icon": "https://raw.githubusercontent.com/"
                    "mayswind/AriaNg/master/src/tileicon.png",
            # "badge": 1,
            # "group": "Aria2",
            # "url": "https://mritd.com"
            },
        "category": "category",
        "sound": "glass.caf"}
    data = json.dumps(data).encode('utf-8')
    req = request.Request(url=url, data=data, headers=headers)
    try:
        request.urlopen(req)
    except Exception:
        print('Faild to send Notification to Bark.')

def push2serverchen(contents):
    '''推送通知到Server酱'''
    send_key = ''
    url = f'https://sctapi.ftqq.com/{send_key}.send'
    headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    data = {"title": 'Arai2', "desp": contents}
    data = bytes(parse.urlencode(data),encoding="utf-8")
    req = request.Request(url=url, data=data, headers=headers)
    try:
        request.urlopen(req)
    except Exception:
        print('Faild to send Notification to ServerChen.')

download_file = get_download_file()
aria2_config= sys.argv[1]
gid = sys.argv[2]
file_num = int(sys.argv[3])
download_path = get_aria2_parameter('dir')
rpc_secret = get_aria2_parameter('rpc-secret')
rpc_listen_port = get_aria2_parameter('rpc-listen-port')
time = str(datetime.datetime.now())[:-7]


