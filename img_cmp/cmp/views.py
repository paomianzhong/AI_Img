from django.shortcuts import render

# Create your views here.
import json
import arrow
import zipfile, os, time, shutil
from django.shortcuts import render, HttpResponse
from django.http import StreamingHttpResponse
from django.shortcuts import render_to_response

from .models import Image, Grade, Performance
from .forms import GradeForm, GradeForm2, GradeForm3
# from .tools import cal_ssim

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
    context = {'form': form, 'numbers': list(range(1, 21)), 'project': project}
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
            imgs = Image.objects.filter(project=project, version=v1, platform=p1, resolution=reso)
            numbers = list(range(1, len(imgs)+1))
            img1 = Image.objects.get(project=project, platform=p1, version=v1, resolution=reso, name__startswith=num)
            img2 = Image.objects.get(project=project, platform=p2, version=v2, resolution=reso, name__startswith=num)
            selected1 = [p1, v1, p2, v2, reso, num]
            context.update({'img1': img1, 'img2': img2, 'numbers': numbers})

        context['selected'] = selected1
        return render(request, 'compare.html', context)
    else:
        if request.GET:
            reso = request.GET['category']
            v1, v2 = request.GET['img1_version'], request.GET['img2_version']
            num = request.GET['number'].zfill(2)
            imgs = Image.objects.filter(project=project, version=v1, resolution=reso)
            numbers = list(range(1, len(imgs)+1))
            img1 = Image.objects.get(project=project, version=v1, resolution=reso, name__startswith=num)
            img2 = Image.objects.get(project=project, version=v2, resolution=reso, name__startswith=num)
            selected2 = [v1, v2, reso, num]
            context.update({'img1': img1, 'img2': img2, 'numbers': numbers})

        if request.POST:
            data = {k: int(v) for k, v in request.POST.items() if k.startswith('dem')}
            data['img'] = Image.objects.get(pk=request.POST['img_id'])
            data['date'] = arrow.arrow.datetime.now()
            data['comment'] = request.POST['comment']
            Grade.objects.create(**data)

        context['selected'] = selected2
        return render(request, 'compare2.html', context)


def compare2(request, project):
    if project == 'Mark':
        form = GradeForm2
        context = {'form': form}
        versions = Image.get_version(project)
        context.update({"versions": versions})
        selected = ['Version', '1']
        numbers = list(range(1, 21))
        if request.GET:
            v = request.GET['img_version']
            imgs = Image.objects.filter(project=project, version=v)
            numbers = list(range(1, len(imgs)+1))
            num = request.GET['number'].zfill(4)
            img = Image.objects.get(project=project, version=v, name__startswith=num)
            context.update({'img': img})
            selected = [v, num]

        if request.POST:
            data = {k: int(v) for k, v in request.POST.items() if k.startswith('dem')}
            data['img'] = Image.objects.get(pk=request.POST['img_id'])
            data['date'] = arrow.arrow.datetime.now()
            data['comment'] = request.POST['comment']
            Grade.objects.create(**data)

        context.update({"numbers": numbers, "selected": selected})
        return render(request, 'compare3.html', context)
    else:
        form = GradeForm3
        context = {'form': form}
        versions = Image.get_version(project)
        context.update({"versions": versions})
        choices = Image.category(project)
        context.update(choices)
        selected = ['Version', 'Category', '1']
        numbers = list(range(1, 21))
        if request.GET:
            reso = request.GET['category']
            v = request.GET['img_version']
            imgs = Image.objects.filter(project=project, version=v, resolution=reso)
            numbers = list(range(1, len(imgs)+1))
            num = request.GET['number'].zfill(2)
            img = Image.objects.get(project=project, version=v, resolution=reso, name__startswith=num)
            context.update({'img': img})
            selected = [v, reso, num]

        if request.POST:
            data = {k: int(v) for k, v in request.POST.items() if k.startswith('dem')}
            data['img'] = Image.objects.get(pk=request.POST['img_id'])
            data['date'] = arrow.arrow.datetime.now()
            data['comment'] = request.POST['comment']
            Grade.objects.create(**data)

        context.update({"numbers": numbers, "selected": selected})
        return render(request, 'compare4.html', context)


def compare_version(request, project):
    choices = Image.category(project)
    context = {}
    context.update(choices)
    numbers = list(range(1, 21))
    selected = ['选择平台', '选择上一版本', '选择当前版本', '类别', 'Number']
    if request.GET:
        p, r = request.GET["platform"], request.GET["category"]
        v1, v2 = request.GET["img1_version"], request.GET["img2_version"]
        num = request.GET["number"].zfill(2)
        imgs = Image.objects.filter(project=project, platform=p, version=v1, resolution=r)
        numbers = list(range(1, len(imgs)+1))
        img1 = Image.objects.get(project=project, platform=p, version=v1, resolution=r, name__startswith=num)
        img2 = Image.objects.get(project=project, platform=p, version=v2, resolution=r, name__startswith=num)
        context.update({"img1": img1, "img2": img2, "project": project})
        selected = [p, v1, v2, r, num]
    context.update({"numbers": numbers, "selected": selected})
    return render(request, 'compare_version.html', context)


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
        base = os.path.basename(zipname)
        zipfilename = os.path.splitext(base)[0]
        localPath = path + '/' + zipfilename
        if not os.path.exists(localPath):
            fz = zipfile.ZipFile(zipname, 'r')
            for file in fz.namelist():
                fz.extract(file, path)
            os.remove(zipname)
        while not os.path.exists(localPath):
            time.sleep(0.1)
        if isrename == '1':
            refilename.refilename(localPath)
            time.sleep(2)
        else:
            pass
        if os.path.exists(path + '/' + '__MACOSX'):
            shutil.rmtree(path + '/' + '__MACOSX')

        if project == 'AI-case' and project == 'Zhaidai_Project':
            upfile.uploadFile(localPath, project, platform, version)
            insertdb.insertdb(localPath, project, platform, version)
            shutil.rmtree(path)
        else:
            upfile.uploadMarkFile(localPath, project, platform, version)
            insertdb.insertdb(localPath, project, platform, version)
            shutil.rmtree(path)
        return HttpResponse("上传完成!")

    else:
        return render(request, "up.html")


def up1(request):
    if request.POST:
        project = request.POST.get('project', '')
        version = request.POST.get('version', '')
        ks3_url = request.POST.get('ks3_url', '')
        insertdb.insertdb1(project, version, ks3_url)
        return HttpResponse("上传完成!")
    else:
        return render(request, "up1.html")


def up2(request):
    if request.POST:
        project = request.POST.get('project', '')
        platform = request.POST.get('platform', '')
        version = request.POST.get('version', '')
        resolution = request.POST.get('resolution', '')
        phone = request.POST.get('phone', '')
        time_avg = request.POST.get('time_avg', '')
        time_max = request.POST.get('time_max', '')
        cpu_avg = request.POST.get('cpu_avg', '')
        cpu_max = request.POST.get('cpu_max', '')
        mem_avg = request.POST.get('mem_avg', '')
        mem_max = request.POST.get('mem_max', '')
        insertdb.insertdb2(project, platform, version, resolution, phone, time_avg, time_max, cpu_avg, cpu_max, mem_avg, mem_max)
        return HttpResponse("上传完成!")
    else:
        return render(request, "up2.html")


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


def update_version(request):
    proj, plat = request.GET['proj'], request.GET['plat']
    versions = Image.get_version(proj, plat)
    dct = {}
    for v in versions:
        dct.update({v: v})
    data = {"versions": dct}
    ret = HttpResponse(json.dumps(data))
    ret['Content-Type'] = 'application/json;charset=uft-8'
    return ret


def update_resolution(request):
    proj, plat, ver = request.GET['proj'], request.GET['plat'], request.GET['ver']
    resolutions = Image.get_resolutions(proj, plat, ver)
    dct = {}
    for r in resolutions:
        dct.update({r: r})
    data = {"resolutions": dct}
    ret = HttpResponse(json.dumps(data))
    ret['Content-Type'] = 'application/json;charset=utf-8'
    return ret


@csrf_exempt
def chart(request,project):
    context = {'project': project}
    choices = Image.category(project)
    context.update(choices)
    selected = ['Category']
    if request.method == 'POST':
        data = []
        ver = request.POST.getlist('img_version')
        reso = request.POST.get('category')
        selected = [reso]
        for v in ver:
            if reso == 'Category':
                g_num, dem1, dem2, dem3, dem4, dem5 = 0, 0, 0, 0, 0, 0
                version_grade = Grade.objects.filter(img__version = v)
                version_dct = {"name": v}
                for g in version_grade:
                    g_num += 1
                    dem1 += g.dem1
                    dem2 += g.dem2
                    dem3 += g.dem3
                    dem4 += g.dem4
                    dem5 += g.dem5

                if g_num != 0:
                    version_dct.update({'data': [round(dem1 / g_num, 2), round(dem2 / g_num, 2), round(dem3 / g_num, 2),
                                                 round(dem4 / g_num, 2), round(dem5 / g_num, 2),
                                                 round((dem1 + dem2 + dem3 + dem4 + dem5) / 5 / g_num, 2)]})
                data.append(version_dct)
            else:
                resolution_grade = Grade.objects.filter(img__version=v, img__resolution=reso)
                resolution_dct = {"name": v + '_' + reso}
                g_num1, dem1, dem2, dem3, dem4, dem5 = 0, 0, 0, 0, 0, 0
                for g in resolution_grade:
                    g_num1 += 1
                    dem1 += g.dem1
                    dem2 += g.dem2
                    dem3 += g.dem3
                    dem4 += g.dem4
                    dem5 += g.dem5
                if g_num1 != 0:
                    resolution_dct.update({'data': [round(dem1 / g_num1, 2), round(dem2 / g_num1, 2), round(dem3 / g_num1, 2),
                                                  round(dem4 / g_num1, 2), round(dem5 / g_num1, 2),
                                                  round((dem1 + dem2 + dem3 + dem4 + dem5) / 5 / g_num1, 2)]})
                data.append(resolution_dct)

        context.update({'series': json.dumps(data)})
        # context.update({'img_version': ver})
        context['img_version'] = ver
    context['selected'] = selected

    return render(request, "chart.html", context)


def chart1(request,project):
    context = {'project': project}
    choices = Image.category(project)
    context.update(choices)
    versions = Image.get_version(project)
    context.update({"versions": versions})
    if project == 'Mark':
        selected = ['Version', '1']
        numbers = list(range(1, 21))
        if request.method == 'POST':
            data = []
            ver = request.POST.get('img_version')
            num = request.POST.get('number').zfill(4)
            try:
                img = Image.objects.get(project=project, version=ver, name__startswith=num)
                selected = [ver, num]
                img_for_grade = Image.objects.get(pk=img.id)
                grades = Grade.objects.filter(img=img_for_grade)
                i = 1
                for g in grades:
                    dct = {"name": "评测"+str(i)}
                    dct.update({"data": [g.dem1, g.dem2, g.dem3, g.dem4]})
                    data.append(dct)
                    i +=1
                context.update({'series': json.dumps(data)})
                print(context)
            except Image.DoesNotExist:
                pass
        context.update({"numbers": numbers, "selected": selected})
        return render(request, "chart2.html", context)
    else:
        selected = ['Version', 'Category', '1']
        numbers = list(range(1, 21))
        if request.method == 'POST':
            data = []
            ver = request.POST.get('img_version')
            reso = request.POST.get('category')
            num = request.POST.get('number').zfill(2)
            img = Image.objects.get(project=project, version=ver, resolution=reso, name__startswith=num)
            selected = [ver, reso, num]
            img_for_grade = Image.objects.get(pk=img.id)
            grades = Grade.objects.filter(img=img_for_grade)
            i = 1
            for g in grades:
                dct = {"name": "评测" + str(i)}
                dct.update({"data": [g.dem1, g.dem2, g.dem3, g.dem4, g.dem5]})
                data.append(dct)
                i += 1
            context.update({'series': json.dumps(data)})
        context.update({"numbers": numbers, "selected": selected})
        return render(request, "chart1.html", context)


def performance(request,project):
    context = {'project': project}
    choices = Performance.category(project)
    context.update(choices)
    platforms = Performance.get_platform(project)
    versions = Performance.get_version(project)
    resolutions = Performance.get_all_resolutions()
    resolutionArray = []
    for item in resolutions:
        resolutionArray.append(item)
    phones = Performance.get_phone(project)
    context.update({"platforms": platforms, "versions": versions, "resolutions": json.dumps(resolutionArray), "phones": phones})
    selected = ['平台', '版本', '机型', '指标']
    context.update({"selected": selected})
    if request.method == 'POST':
        time_data = []
        cpu_data = []
        mem_data = []
        plat = request.POST.get('img_platform')
        ver = request.POST.getlist('img_version')
        phone = request.POST.getlist('phone')
        selected = [plat, ver, phone]
        context.update({"resolutions": json.dumps(resolutionArray)})
        for i in range(0, len(ver)):
            time_avg_list = []
            time_max_list = []
            cpu_avg_list = []
            cpu_max_list = []
            mem_avg_list = []
            mem_max_list = []
            for j in range(0, len(phone)):
                performance = Performance.objects.filter(project=project, platform=plat, version=ver[i], phone=phone[j])
                for p in performance:
                    time_avg = p.time_avg
                    time_avg_list.append(str(time_avg))
                    time_max = p.time_max
                    time_max_list.append(str(time_max))

                    cpu_avg = p.cpu_avg
                    cpu_avg_list.append(str(cpu_avg))
                    cpu_max = p.time_max
                    cpu_max_list.append(str(cpu_max))

                    mem_avg = p.mem_avg
                    mem_avg_list.append(str(mem_avg))
                    mem_max = p.mem_max
                    mem_max_list.append(str(mem_max))

                dct = {"name": ver[i]+'_'+phone[j] + "_time_avg"}
                dct.update({'data': [float(time_avg_list[0]), float(time_avg_list[1])]})
                time_data.append(dct)
                dct = {"name": ver[i] + '_' + phone[j] + "_time_max"}
                dct.update({'data': [float(time_max_list[0]), float(time_max_list[1])]})
                time_data.append(dct)
                context.update({'time_series': json.dumps(time_data)})

                dct = {"name": ver[i] + '_' + phone[j] + "_cpu_avg"}
                dct.update({'data': [float(cpu_avg_list[0]), float(cpu_avg_list[1])]})
                cpu_data.append(dct)
                dct = {"name": ver[i] + '_' + phone[j] + "_cpu_max"}
                dct.update({'data': [float(cpu_max_list[0]), float(cpu_max_list[1])]})
                cpu_data.append(dct)
                context.update({'cpu_series': json.dumps(cpu_data)})

                dct = {"name": ver[i] + '_' + phone[j] + "_mem_avg"}
                dct.update({'data': [float(mem_avg_list[0]), float(mem_avg_list[1])]})
                mem_data.append(dct)
                dct = {"name": ver[i] + '_' + phone[j] + "_mem_max"}
                dct.update({'data': [float(mem_max_list[0]), float(mem_max_list[1])]})
                mem_data.append(dct)
                context.update({'mem_series': json.dumps(mem_data)})

    context.update({"selected": selected})
    return render(request, "performance.html", context)