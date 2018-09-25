from django.shortcuts import render

# Create your views here.
import json
import arrow
import zipfile,os,time,shutil
from django.shortcuts import render, HttpResponse
from django.http import StreamingHttpResponse
from django.shortcuts import render_to_response

from .models import Image, Grade
from .forms import GradeForm, GradeForm2

from django.views.decorators.csrf import csrf_exempt
from . import upfile
from . import insertdb
from . import refilename


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


def grade(request,pid):
    data = []
    g_num, dem1, dem2, dem3, dem4, dem5 = 0, 0, 0, 0, 0, 0
    # pid = request.GET['']
    v = request.GET['version']
    c = request.GET['category']
    img = Image.objects.get(pk=pid)
    version_imgs = Image.objects.filter(version=v)
    # print("version img "+type(version_imgs))
    resolution_imgs = Image.objects.filter(version=v, resolution=c)
    dct = {"version": img.name}
    grades = Grade.objects.filter(img=img)
    ver_imgs = ""
    res_imgs = ""
    for item in version_imgs:
        ver_imgs += str(item.id) + ","
    ver_imgs = ver_imgs[0:-1]
    for item in resolution_imgs:
        res_imgs += str(item.id) + ","
    res_imgs = res_imgs[0:-1]
    version_grades = Grade.objects.extra(where=['img_id IN ('+ ver_imgs +')'])
    resolution_grades = Grade.objects.extra(where=['img_id IN ('+ res_imgs +')'])
    # cgrades = Grade.objects.filter(img=imgs)
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

    version_dct = {"version": "v_"+v}
    for g in version_grades:
        g_num += 1
        dem1 += g.dem1
        dem2 += g.dem2
        dem3 += g.dem3
        dem4 += g.dem4
        dem5 += g.dem5
    if g_num != 0:
        version_dct.update({"dem1": round(dem1/g_num, 2), "dem2": round(dem2/g_num, 2), "dem3": round(dem3/g_num, 2),
                    "dem4": round(dem4/g_num, 2), "dem5": round(dem5/g_num, 2)})
    data.append(version_dct)
    resolution_dct = {"version": "c_"+c}
    for g in resolution_grades:
        g_num += 1
        dem1 += g.dem1
        dem2 += g.dem2
        dem3 += g.dem3
        dem4 += g.dem4
        dem5 += g.dem5
    if g_num != 0:
        resolution_dct.update(
            {"dem1": round(dem1 / g_num, 2), "dem2": round(dem2 / g_num, 2), "dem3": round(dem3 / g_num, 2),
             "dem4": round(dem4 / g_num, 2), "dem5": round(dem5 / g_num, 2)})
    data.append(resolution_dct)
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


def up(request):
    if request.POST:
        isrename = request.POST.get('rename','')
        project = request.POST.get('project', '')
        print("isrename:"+isrename)
        platform = request.POST.get('platform', '')
        version = request.POST.get('version', '')
        # 修改上传目录
        # path = '/Users/zhangminghui/Documents/AI_Img/img_cmp/upload'
        path = '/home/eva/AI_Img/img_cmp/upload'
        zipname = path + '/' + os.listdir(path)[0]
        fz = zipfile.ZipFile(zipname, 'r')
        for file in fz.namelist():
            fz.extract(file, path)
        base = os.path.basename(zipname)
        zipfilename = os.path.splitext(base)[0]
        localPath = path+'/' + zipfilename
        while not os.path.exists(localPath):
            time.sleep(0.2)
        if isrename == '1':
            refilename.refilename(localPath)
        else:
            pass
        shutil.rmtree(path + '/' + '__MACOSX')
        os.remove(zipname)
        if project == 'Mark':
            upfile.uploadMarkFile(localPath, project, version)
            insertdb.insertdb(localPath, project, platform, version)
            shutil.rmtree(path)
        else:
            upfile.uploadFile(localPath, project, platform, version)
            insertdb.insertdb(localPath, project, platform, version)
            shutil.rmtree(path)
        return HttpResponse("上传完成!")

    else:
        return render(request, "up.html")


def export(request):
    p, v = request.GET['proj'], request.GET['ver']
    content = Image.export_xls(proj=p, ver=v)
    response = HttpResponse(content)
    response['Content-Type'] = 'application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="{}.xls"'.format(v)
    # if p == 'Mark':
    #     content = Image.export_xls(proj=p, ver=v)
    #     response = HttpResponse(content)
    #     response['Content-Type'] = 'application/vnd.ms-excel'
    #     response['Content-Disposition'] = 'attachment;filename="{}.xls"'.format(v)
    # else:
    #     category = request.GET['cat']
    #     content = Image.export_xls2(proj=p, ver=v, cat=category)
    #     response = HttpResponse(content)
    #     response['Content-Type'] = 'application/vnd.ms-excel'
    #     response['Content-Disposition'] = 'attachment;filename="{}.xls"'.format(v)
    return response


@csrf_exempt
def fileupload(request):
    if request.method == 'POST':
        upload_file = request.FILES.get('file')
        task = request.POST.get('task_id')  # 获取文件唯一标识符
        chunk = request.POST.get('chunk', 0)  # 获取该分片在所有分片中的序号
        filename = '%s%s' % (task, chunk)  # 构成该分片唯一标识符
        print("filename=",filename)
        tempDir = './upload/'
        if not os.path.exists(tempDir):
            os.mkdir(tempDir)
        path = tempDir + filename
        f = open(path, 'wb')
        f.write(upload_file.read())
        f.close()
    return render_to_response('upload2.html', locals())


def fileMerge(request):
    print(request.GET)
    task = request.GET.get('task_id')
    ext = request.GET.get('filename', '')
    name = request.GET.get('filename', '')
    print(ext)
    upload_type = request.GET.get('type')
    if len(ext) == 0 and upload_type:
        ext = upload_type.split('/')[1]
    ext = '' if len(ext) == 0 else '.%s' % ext  # 构建文件后缀名
    chunk = 0
    with open('./upload/%s' % (name), 'wb') as target_file:  # 创建新文件
        while True:
            try:
                filename = './upload/%s%d' % (task, chunk)
                source_file = open(filename, 'rb')  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
            except IOError:
                break
            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间
    return render_to_response('upload2.html',locals())



