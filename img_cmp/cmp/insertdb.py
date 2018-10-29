#/user/bin/python
# -*- coding:UTF-8 -*-

import requests
import os


def insertdb(localPath, project, platform, version):
    if project == 'AI-case' and project == 'Zhaidai_Project':
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
                    requests.get('http://10.100.51.45:8000/api/insert', params=payload)

    else:
        for dirs in os.walk(localPath):
            for file in dirs[2]:
                payload = {'name': file,
                           'project': project,
                           'platform': platform,
                           'version': version,
                           'resolution': 'random',
                           's3_url': 'https://ks3-cn-beijing.ksyun.com/qa-vod/' + project + '/' + platform + '/' +
                                     version + '/' + file}
                requests.get('http://10.100.51.45:8000/api/insert', params=payload)


def insertdb1(project, version, ks3_url):
    payload = {'name': ks3_url.split('/')[-1],
               'project': project,
               'version': version,
               's3_url': ks3_url}
    requests.get('http://10.100.51.45:8000/api/insert', params=payload)


def insertdb2(project, platform, version, resolution, phone, time_avg, time_max, cpu_avg, cpu_max, mem_avg, mem_max):
    payload = {
        'project': project,
        'platform': platform,
        'version': version,
        'resolution': resolution,
        'phone': phone,
        'time_avg': time_avg,
        'time_max': time_max,
        'cpu_avg': cpu_avg,
        'cpu_max': cpu_max,
        'mem_avg': mem_avg,
        'mem_max': mem_max
    }
    requests.get('http://10.100.51.45:8000/api/insert1', params=payload)

