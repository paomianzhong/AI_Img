#/user/bin/python
# -*- coding:UTF-8 -*-


import os,urllib
from . import upload


'''下载文件'''
def downFile(localPath,ks3Path):
	resolution = os.listdir(localPath)
	count = len(resolution)
	for i in range(count):
		file_dir = localPath + '/' + resolution[i]
		for dirs in os.walk(file_dir):
			for file in dirs[2]:
				filePath = localPath + '/' + resolution[i] + '/' + file

				'''上传已下载的文件'''
				rr=upload.upload()
				rr.objectKey = ks3Path+'/' +file #上传路径
				print(rr.objectKey)
				# rr.objectKey = 'xiexiaoli-case/AI-case/test' + '/' + fileName  # 上传路径
				rr.filePath = filePath
				rr.bucket = 'qa-vod' #上传bucket
				rr.ak = 'AKLTzSNRzrm5QeOAl95nkERhqA'
				rr.sk = 'OFRC8ECyyUexud8S36QI4xTXNqyXZeAo2MBivflzZW6MKxkZ5R8/gLJPLsf6smu2fg=='
				ret = rr.uploadSingleFile()
				print("Start uploading files: %s ,status:%d " % (filePath,ret))


if __name__ == '__main__':
	pass

