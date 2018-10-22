import os
import ssim
import requests
from pathlib import Path
from contextlib import contextmanager


@contextmanager
def cal_ssim(url_i1, url_i2):
    tmp_path = Path(__file__).absolute().parent.parent/'tmp'
    img_name1 = url_i1.rpartition('/')[-1]
    img_name2 = url_i2.rpartition('/')[-1]
    contrast = str(tmp_path/img_name1)
    data = requests.get(url_i1)
    with open(contrast,'wb') as f:
        f.write(data.content)
    target = str(tmp_path/img_name2)
    data = requests.get(url_i2)
    with open(target,'wb') as f:
        f.write(data.content)
    ret = ssim.compute_ssim(contrast, target)
    yield ret
    for p in tmp_path.glob('*'):
        os.remove(str(p))

if __name__ == '__main__':
    url1 = 'https://ks3-cn-beijing.ksyun.com/qa-vod/Mark/miaopai_cover_image_jpg/0072_142_0_miaopai_jpg_199.jpg'
    url2 = 'https://ks3-cn-beijing.ksyun.com/qa-vod/Mark/miaopai_cover_image_jpg/0004_176_0_miaopai_jpg_199.jpg'
    with cal_ssim(url1, url2) as v:
        print(v)
