from django.shortcuts import render

# Create your views here.
import json
from django.shortcuts import render, HttpResponse

from .models import Image, Grade
from .forms import GradeForm


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
        num = int(request.GET['number'])
        img1 = Image.objects.filter(platform=p1, version=v1, resolution=reso)[num-1]
        img2 = Image.objects.filter(platform=p2, version=v2, resolution=reso)[num-1]
        selected = [p1, v1, p2, v2, reso, num]
        context.update({'img1': img1, 'img2': img2})

    if request.POST:
        data = {k: int(v) for k, v in request.POST.items() if k.startswith('dem')}
        data['comment'] = request.POST['comment']
        data['img'] = Image.objects.get(pk=request.POST['img_id'])
        Grade.objects.create(**data)

    context['selected'] = selected
    return render(request, 'index.html', context)


def grade(request, pid):
    if request.POST:
        print(request.POST)


