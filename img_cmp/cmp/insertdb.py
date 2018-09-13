#/user/bin/python
# -*- coding:UTF-8 -*-

import requests
import os

def insertdb(localPath,project,platform,version,ks3Path):
    resolution = os.listdir(localPath)
    count = len(resolution)
    for i in range(count):
        file_dir = localPath + '/' + resolution[i]
        for dirs in os.walk(file_dir):
            for file in dirs[2]:
                payload = {'name':file,
                           'project':project,
                           'platform':platform,
                           'version':version,
                           'resolution':resolution[i],
                           's3_url':'https://ks3-cn-beijing.ksyun.com/qa-vod/'+ks3Path+'/' + resolution[i] + '/' + file}
                print(payload)
                requests.get('http://127.0.0.1:8000/insert',params=payload)

