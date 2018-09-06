from django.shortcuts import render

# Create your views here.
import json
from django.shortcuts import render, HttpResponse

from .models import Image, Grade
from .forms import GradeForm
import arrow


def index(request):
    form = GradeForm
    context = {'form': form, 'numbers': list(range(1, 21))}
    choices = Image.category()
    context.update(choices)
    selected = ['Platform', 'Version', 'Platform', 'Version', 'Resolution', 'Number']

    if request.GET:
        reso = request.GET['resolution']
        p1, v1 = request.GET['img1_platform'], request.GET['img1_version']
        p2, v2 = request.GET['img2_platform'], request.GET['img2_version']
        num = request.GET['number'].zfill(2)
        img1 = Image.objects.get(platform=p1, version=v1, resolution=reso, name__startswith=num)
        img2 = Image.objects.get(platform=p2, version=v2, resolution=reso, name__startswith=num)
        selected = [p1, v1, p2, v2, reso, num]
        context.update({'img1': img1, 'img2': img2})

    if request.POST:
        data = {k: int(v) for k, v in request.POST.items() if k.startswith('dem')}
        data['img'] = Image.objects.get(pk=request.POST['img_id'])
        data['date'] = arrow.now().isoformat().split('.')[0]
        Grade.objects.create(**data)
        # grades = Grade.objects.filter(img=data['img'])
        # context.update({'grades': grades})

    context['selected'] = selected
    return render(request, 'index.html', context)


def grade(request, pid):
    data = []
    dct = {}
    if request.GET:
        if pid:
            grades = Grade.objects.filter(img=Image.objects.get(pk=pid))
            for g in grades:
                # print(g.date.strftime('%Y-%m-%d %H:%M:%S'))
                dct['date'] = g.date.strftime('%Y-%m-%d %H:%M:%S')
                dct['dem1'] = g.dem1
                dct['dem2'] = g.dem2
                dct['dem3'] = g.dem3
                dct['dem4'] = g.dem4
                dct['dem5'] = g.dem5
                temp = dct.copy()
                data.append(temp)
            return HttpResponse(json.dumps(data))