from django.shortcuts import render

# Create your views here.
import json
import arrow
import zipfile,os,time,shutil
from django.shortcuts import render, HttpResponse
from django.http import StreamingHttpResponse

from .models import Image, Grade
from .forms import GradeForm, GradeForm2

from . import upfile
from . import insertdb


def index(request):
    projects = Image.get_project()
    context = {'projects': projects}
    return render(request, 'index.html', context)


def compare(request, project):
    form = GradeForm
    context = {'form': form, 'numbers': list(range(1, 21))}
    choices = Image.category(project)
    context.update(choices)
    selected1 = ['Platform', 'Version', 'Platform', 'Version', 'Resolution', '1']
    selected2 = ['Version', 'Version', 'Category', '1']
    if project == 'AI-case':
        if request.GET:
            reso = request.GET['resolution']
            p1, v1 = request.GET['img1_platform'], request.GET['img1_version']
            p2, v2 = request.GET['img2_platform'], request.GET['img2_version']
            num = request.GET['number'].zfill(2)
            img1 = Image.objects.get(project=project, platform=p1, version=v1, resolution=reso, name__startswith=num)
            img2 = Image.objects.get(project=project, platform=p2, version=v2, resolution=reso, name__startswith=num)
            selected1 = [p1, v1, p2, v2, reso, num]
            context.update({'img1': img1, 'img2': img2})

        context['selected'] = selected1
        return render(request, 'compare.html', context)
    else:
        if request.GET:
            reso = request.GET['category']
            v1, v2 = request.GET['img1_version'], request.GET['img2_version']
            num = request.GET['number'].zfill(2)
            img1 = Image.objects.get(project=project, version=v1, resolution=reso, name__startswith=num)
            img2 = Image.objects.get(project=project, version=v2, resolution=reso, name__startswith=num)
            selected2 = [v1, v2, reso, num]
            context.update({'img1': img1, 'img2': img2})

        if request.POST:
            data = {k: int(v) for k, v in request.POST.items() if k.startswith('dem')}
            data['img'] = Image.objects.get(pk=request.POST['img_id'])
            data['date'] = arrow.arrow.datetime.now()
            Grade.objects.create(**data)

        context['selected'] = selected2
        return render(request, 'compare2.html', context)


def compare2(request, project):
    form = GradeForm2
    context = {'form': form}
    versions = Image.get_version(project)
    context.update({"versions": versions})
    selected = ['Version', '1']
    numbers = list(range(1, 21))

    if request.GET:
        v = request.GET['img_version']
        imgs = Image.objects.filter(project=project, version=v)
        numbers = list(range(1, len(imgs) + 1))
        num = request.GET['number'].zfill(2)
        img = Image.objects.get(project=project, version=v, name__startswith=num)
        context.update({'img': img})
        selected = [v, num]

    if request.POST:
        data = {k: int(v) for k, v in request.POST.items() if k.startswith('dem')}
        data['img'] = Image.objects.get(pk=request.POST['img_id'])
        data['date'] = arrow.arrow.datetime.now()
        Grade.objects.create(**data)

    context.update({"numbers": numbers, "selected": selected})
    return render(request, 'compare3.html', context)


def grade(request, pid):
    data = []
    g_num, dem1, dem2, dem3, dem4, dem5 = 0, 0, 0, 0, 0, 0
    img = Image.objects.get(pk=pid)
    dct = {"version": img.version}
    grades = Grade.objects.filter(img=img)
    for g in grades:
        g_num += 1
        dem1 += g.dem1
        dem2 += g.dem2
        dem3 += g.dem3
        dem4 += g.dem4
        dem5 += g.dem5
    if g_num != 0:
        dct.update({"dem1": round(dem1/g_num, 2), "dem2": round(dem2/g_num, 2), "dem3": round(dem3/g_num, 2),
                    "dem4": round(dem4/g_num, 2), "dem5": round(dem5/g_num, 2)})
    data.append(dct)
    return HttpResponse(json.dumps(data))


def grade2(request, pid):
    data = []
    img = Image.objects.get(pk=pid)
    grades = Grade.objects.filter(img=img)
    for g in grades:
        dct = {}
        dct.update({"date": g.date.strftime("%Y-%m-%d %H:%M:%S"), "dem1": g.dem1, "dem2": g.dem2, "dem3": g.dem3, "dem4": g.dem4})
        data.append(dct)
    return HttpResponse(json.dumps(data))


def insert(request):
    try:
        data = request.GET.dict()
        Image.objects.create(**data)
        return HttpResponse(json.dumps({'result': 'ok'}))
    except Exception as e:
        return HttpResponse(json.dumps({'result': e}))


def upload(request):
    if request.POST:
        project = request.POST.get('project', None)
        print("project"+project)
        platform = request.POST.get('platform', '')
        version = request.POST.get('version', '')
        # 修改上传目录
        # path = '/Users/zhangminghui/Project/AI_Img/img_cmp/cmp/image_set'
        path = '/home/eva/AI_Img/img_cmp/image_set'
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            os.mkdir(path)
            print(path + ' 创建成功')

        # 获取上传的文件，如果没有文件，则默认为None
        File = request.FILES.get("myfile", None)
        if File is None:
            return HttpResponse("没有需要上传的文件")
        else:

            with open("./cmp/image_set/%s" % File.name, 'wb+') as f:
                # 分块写入文件
                for chunk in  File.chunks():
                    f.write(chunk)

            filename = path+'/'+File.name
            fz = zipfile.ZipFile(filename, 'r')
            for file in fz.namelist():
                fz.extract(file, path)
            base = os.path.basename(filename)
            zipfilename = os.path.splitext(base)[0]
            localPath = path+'/' + zipfilename
            while not os.path.exists(localPath):
                time.sleep(2)
            upfile.uploadFile(localPath, project, platform,version)
            insertdb.insertdb(localPath, project,platform, version)
            shutil.rmtree(path)
            return HttpResponse("上传完成!")

    else:
        return render(request, "upload.html")


def export(request):
    p, v = request.GET['proj'], request.GET['ver']
    content = Image.export_xls(proj=p, ver=v)
    response = HttpResponse(content)
    response['Content-Type'] = 'application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="{}.xls"'.format(v)
    return response

