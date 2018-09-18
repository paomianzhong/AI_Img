#/user/bin/python
# -*- coding:UTF-8 -*-


import os,urllib
from . import upload


def uploadFile(localPath,project,platform,version):
	resolution = os.listdir(localPath)
	count = len(resolution)
	print("project" + project)
	for i in range(count):
		file_dir = localPath + '/' + resolution[i]
		for dirs in os.walk(file_dir):
			for file in dirs[2]:
				filePath = localPath + '/' + resolution[i] + '/' + file

				'''上传文件'''
				rr=upload.upload()
				if platform.strip() == '':
					# 上传路径
					rr.objectKey = project + '/' + version+'/' + resolution[i]+'/' + file

				else:
					rr.objectKey = project + '/' + platform + '/' + version + '/' + resolution[i] + '/' + file  # 上传路径
				print("KS3路径："+rr.objectKey)
				rr.filePath = filePath
				rr.bucket = 'qa-vod' #上传bucket
				rr.ak = 'AKLTzSNRzrm5QeOAl95nkERhqA'
				rr.sk = 'OFRC8ECyyUexud8S36QI4xTXNqyXZeAo2MBivflzZW6MKxkZ5R8/gLJPLsf6smu2fg=='
				ret = rr.uploadSingleFile()
				print("Start uploading files: %s ,status:%d " % (filePath,ret))


if __name__ == '__main__':
	pass


