#/user/bin/python
# -*- coding:UTF-8 -*-

import requests
import os

def insertdb(localPath, project, platform, version):
    if project == 'Mark':
        for dirs in os.walk(localPath):
            for file in dirs[2]:
                payload = {'name': file,
                           'project': project,
                           'version': version,
                           's3_url': 'https://ks3-cn-beijing.ksyun.com/qa-vod/' + project + '/' +
                                     version + '/' + file}
                requests.get('http://10.100.51.45:8020/insert', params=payload)
    else:
        resolution = os.listdir(localPath)
        count = len(resolution)
        for i in range(count):
            file_dir = localPath + '/' + resolution[i]
            for dirs in os.walk(file_dir):
                for file in dirs[2]:
                    if platform.strip() == '':
                        payload = {'name': file,
                                   'project': project,
                                   'version': version,
                                   'resolution': resolution[i],
                                   's3_url': 'https://ks3-cn-beijing.ksyun.com/qa-vod/' + project + '/' +
                                             version+'/' + resolution[i] + '/' + file}

                    else:
                        payload = {'name': file,
                                   'project': project,
                                   'platform': platform,
                                   'version': version,
                                   'resolution': resolution[i],
                                   's3_url': 'https://ks3-cn-beijing.ksyun.com/qa-vod/' + project + '/' + platform + '/' +
                                             version + '/' + resolution[i] + '/' + file}
                    requests.get('http://10.100.51.45:8020/insert', params=payload)

