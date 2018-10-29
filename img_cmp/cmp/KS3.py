import pdb
import hmac
import base64
import hashlib
import pathlib
import os
from itertools import chain
import arrow
import requests

import asyncio
from aiohttp import ClientSession


class KS3:
    def __init__(self, host):
        self.host = host
        self.ak = 'AKLTzSNRzrm5QeOAl95nkERhqA'
        self.sk = b'OFRC8ECyyUexud8S36QI4xTXNqyXZeAo2MBivflzZW6MKxkZ5R8/gLJPLsf6smu2fg=='
        self.content_md5 = ''
        self.content_type = 'application/vnd.apple.mpegurl'
        self.acl = 'public-read'
        self.deal = '1'
        pass

    def _sign(self, url):
        expire = str(arrow.now().shift(hours=1).timestamp)
        # expire = '1540439476'
        acl = f'x-kss-acl:{self.acl}'
        deal = f'x-kss-meta-videodeal:{self.deal}'
        lst = ['PUT', self.content_md5, self.content_type, expire, acl, deal, url]
        presigned = '\n'.join(lst).encode('utf-8')
        data = hmac.new(self.sk, presigned, hashlib.sha1).digest()
        signature = base64.b64encode(data)
        print(signature)
        ret ={
            'KSSAccessKeyId': self.ak,
            'Expires': expire,
            'Signature': signature.decode('utf-8')
        }
        return ret

    async def upload(self, session, url, data):
        """
        upload file to KS3 server.
        :param session: aiohttp session
        :param url: url path
        :param data: binary image data
        :return: ok
        """
        para = self._sign(url)
        head = {
            'Content-Type': self.content_type,
            'x-kss-acl': self.acl,
            'x-kss-meta-videodeal': self.deal,
            'Content-Length': str(len(data))
        }
        return await session.put(self.host+url, headers=head, params=para, data=data)

    async def upload_file(self, anchor, file):
        async with ClientSession() as session:
            path = pathlib.Path(file)
            data = path.read_bytes()
            url = anchor + path.name
            return await self.upload(session, url, data)

    async def upload_dir(self, anchor, directory):
        path = pathlib.Path(directory)
        ret = []
        async with ClientSession() as session:
            for p in chain(path.rglob('*.jpg'), path.rglob('*.png'), path.rglob('*.gif')):
                data = p.read_bytes()
                url = anchor + p.relative_to(path).as_posix()
                resp = await self.upload(session, url, data)
                ret.append(resp)
        return ret


if __name__ == '__main__':
    url = 'http://httpbin.org/delay/2'
#   requests.get(url)
    loop = asyncio.get_event_loop()
    # tasks = []
    # for i in range(5):
    #     task = asyncio.ensure_future(hello(url))
    #     tasks.append(task)
    # loop.run_until_complete(asyncio.wait(tasks))
    # print(tasks[0].result())

    host = "http://ks3-cn-beijing.ksyun.com"
    path = '/qa-vod/upload_test/'
    k=KS3(host)
    # k._sign(path)
    with open('Pipfile', 'rb') as f:
        file = f.read()
    # pdb.set_trace()
    # k.test_upload(path, file)
#   task = asyncio.ensure_future(k.upload_file(path, file))
    task = asyncio.ensure_future(k.upload_dir(path, '.'))
    loop.run_until_complete(task)
    pdb.set_trace()
#   print(task.result())

