import json
from django.shortcuts import render, HttpResponse
import arrow

from .models import Image, Grade
from .tools import cal_ssim


def insert(request):
    """
    插入新的图片信息到数据库
    """
    try:
        data = request.GET.dict()
        Image.objects.create(**data)
        return HttpResponse(json.dumps({'result': 'ok'}))
    except Exception as e:
        return HttpResponse(json.dumps({'result': e}))


def grade(request, pid):
    # 打分
    if request.method == 'POST':
        data = {k: int(v) for k, v in request.POST.items() if k.startswith('dem')}
        data['img'] = Image.objects.get(pk=pid)
        data['date'] = arrow.arrow.datetime.now()
        data['comment'] = request.POST['comment']
        Grade.objects.create(**data)
        return HttpResponse(json.dumps({'result': 'ok'}))
    # 获取平均分
    if request.method == 'GET':
        img = Image.objects.get(pk=pid)
        data = []
        data.append(Grade.get_average(img))
        data.append(Grade.get_average(img, category=True))
        data.append(Grade.get_average(img, version=True))
        return HttpResponse(json.dumps(data))


def grade2(request, pid):
    """获取图片的评分记录"""
    data = []
    img = Image.objects.get(pk=pid)
    grades = Grade.objects.filter(img=img)
    for g in grades:
        dct = {}
        dct.update({"date": g.date.strftime("%Y-%m-%d %H:%M:%S"), "dem1": g.dem1, "dem2": g.dem2, "dem3": g.dem3, "dem4": g.dem4})
        data.append(dct)
    return HttpResponse(json.dumps(data))


def get_ssim(request):
    """
    获取两张图片的ssim值
    """
    try:
        data = request.GET.dict()
        img1 = Image.objects.get(pk=data['img1'])
        img2 = Image.objects.get(pk=data['img2'])
        with cal_ssim(img1.s3_url, img2.s3_url) as v:
            return HttpResponse(json.dumps({'ssim': v}))
    except Exception as e:
        return HttpResponse(json.dumps({'msg': e}))


def evaluate(request, pid):
    """
    评价图片是否优于上一个版本 1: 是, -1: 否
    """
    try:
        data = request.POST['ifimproved']
        img = Image.objects.get(pk=pid)
        img.add_improved(data)
        return HttpResponse(json.dumps({'result': 'ok'}))
    except Exception as e:
        return HttpResponse(json.dumps({'result': e}))


def export(request):
    p, v = request.GET['proj'], request.GET['ver']
    content = Image.export_xls(proj=p, ver=v)
    response = HttpResponse(content)
    response['Content-Type'] = 'application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="{}.xls"'.format(v)
    return response

