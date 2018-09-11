from django.shortcuts import render

# Create your views here.
import json
import arrow
from django.shortcuts import render, HttpResponse

from .models import Image, Grade
from .forms import GradeForm


def index(request):
    projects = Image.get_project()
    context = {'projects': projects}
    return render(request, 'index.html', context)


def compare(request, project):
    form = GradeForm
    context = {'form': form, 'numbers': list(range(1, 21))}
    choices = Image.category(project)
    context.update(choices)
    selected1 = ['Platform', 'Version', 'Platform', 'Version', 'Resolution', 'Number']
    selected2 = ['Version', 'Version', 'Category', 'Number']
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


def grade(request, pid):
    dct = {}
    data = []
    g_num, dem1, dem2, dem3, dem4, dem5 = 0, 0, 0, 0, 0, 0
    img = Image.objects.get(pk=pid)
    grades = Grade.objects.filter(img=img)
    for g in grades:
        g_num += 1
        dem1 += g.dem1
        dem2 += g.dem2
        dem3 += g.dem3
        dem4 += g.dem4
        dem5 += g.dem5
    if g_num != 0:
        dct = {"dem1": dem1/g_num, "dem2": dem2/g_num, "dem3": dem3/g_num, "dem4": dem4/g_num, "dem5": dem5/g_num}
    data.append(dct)
    return HttpResponse(json.dumps(data))