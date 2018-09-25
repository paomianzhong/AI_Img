#/user/bin/python
# -*- coding:UTF-8 -*-

import os
import zipfile

def refilename(path):
    filelist = os.listdir(path)
    total_num = len(filelist)
    i = 1
    for item in filelist:
        if item.endswith('.png'):
            src = os.path.join(os.path.abspath(path), item)
            dst = os.path.join(os.path.abspath(path), '0'+format(str(i), '0>3s') + '.png')
            os.rename(src, dst)
            print('converting %s to %s ...' % (src, dst))
            i = i + 1
    j = i
    for item in filelist:
        if item.endswith('.jpg'):
            src = os.path.join(os.path.abspath(path), item)
            dst = os.path.join(os.path.abspath(path), '0'+format(str(j), '0>3s') + '.jpg')
            os.rename(src, dst)
            print('converting %s to %s ...' % (src, dst))
            j = j + 1
    k = j
    for item in filelist:
        if item.endswith('.jpeg'):
            src = os.path.join(os.path.abspath(path), item)
            dst = os.path.join(os.path.abspath(path), '0'+format(str(j), '0>3s') + '.jpeg')
            os.rename(src, dst)
            print('converting %s to %s ...' % (src, dst))
            k = k + 1
    print('total %d to rename & converted %d jpgs' % (total_num, k-1))


def zip_file(path,zipname):
    file_news = zipname + '.zip'  # 压缩后文件夹的名字
    z = zipfile.ZipFile(os.path.dirname(path)+'/'+file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
    for dirpath,dirnames,filenames in os.walk(path):
        fpath = dirpath.replace(path, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
              z.write(os.path.join(dirpath, filename), fpath+filename)
        print('压缩成功')
    z.close()
