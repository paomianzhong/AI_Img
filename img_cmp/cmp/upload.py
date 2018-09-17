#/user/bin/python
# -*- coding:UTF-8 -*-
import hmac
import hashlib
import requests
import os
import time
import urllib
import base64
import six
import shutil
import json
#import off_config
class upload(object):
    host="ks3-cn-beijing.ksyun.com"
    verb="PUT"
    expire=int(time.time())+3600
    bucket=""
    objectKey= ""
    ak=""
    sk=""
    contentMD5 = ""
    contentType = "application/vnd.apple.mpegurl"
    acl = "public-read"
    metaDeal = "1"
    filePath = ""
    def genKS3SignedString(self):
        if self.host == "" or self.verb == "" or self.expire <= 0 or self.bucket == "" or self.objectKey == "":
            return ""
        signedURL = "http://" + self.host + "/" + self.bucket + "/" + self.objectKey
        if self.ak == "" or self.sk == "":
            return signedURL
        presigned = self.verb+'\n'
        presigned += self.contentMD5+"\n"
        presigned += self.contentType+"\n"
        presigned += str(self.expire)+"\n"
        if self.acl != "" :
            presigned += "x-kss-acl:" + self.acl + "\n"
        if self.metaDeal != "" :
            presigned += "x-kss-meta-videodeal:" + self.metaDeal + "\n"
        presigned += "/" + self.bucket + "/" + self.objectKey
        if isinstance(self.sk,six.text_type):
            self.sk = self.sk.encode(encoding="utf-8")
        if isinstance(presigned,six.text_type):
            presigned = presigned.encode(encoding="utf-8")
        signature = base64.b64encode(hmac.new(self.sk,presigned,hashlib.sha1).digest())
        param = list()
        param.append(('KSSAccessKeyId',self.ak))
        param.append(('Expires',self.expire))
        param.append(('Signature',signature))
        signedURL += "?"+urllib.parse.urlencode(param)
        return signedURL
    def uploadSingleFile(self):
        status_code = 0
        if self.filePath == "":
            print("file no exist")
            return status_code        
        url = self.genKS3SignedString()
        if url == "":
            print("genKS3SignedString failed")
            return status_code
        file_data = ""
        #file_object = open("/Users/zhangminghui/Documents/AI/test1")
        file_object = open(self.filePath,'rb')
        try:
            file_data = file_object.read()
        finally:
            file_object.close()
            if file_data == "":
                print("open file failed")
                return status_code
        header = {}
        header["Content-Type"] = self.contentType
        header["x-kss-acl"] = self.acl
        header["x-kss-meta-videodeal"] = self.metaDeal
        header["Content-Length"] = str(os.path.getsize(self.filePath))
        s = requests.session()
        s.headers = header
        r  = s.put(url, file_data)
        status_code = r.status_code
        return status_code

if __name__ == "__main__":
	pass
