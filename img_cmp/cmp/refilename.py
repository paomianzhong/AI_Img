#/user/bin/python
# -*- coding:UTF-8 -*-

import os
import zipfile

def refilename(path):
    filelist = os.listdir(path)
    i = 1
    for item in filelist:
        filename = os.path.splitext(item)[0]  # 文件名
        filetype = os.path.splitext(item)[1]  # 文件扩展名
        src = os.path.join(os.path.abspath(path), item)
        if i < 1000:
            dst = os.path.join(os.path.abspath(path), '0'+format(str(i), '0>3s') + '_' + filename + filetype)
        else:
            dst = os.path.join(os.path.abspath(path), format(str(i), '0>3s') + '_' + filename + filetype)
        os.rename(src, dst)
        i = i + 1


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
