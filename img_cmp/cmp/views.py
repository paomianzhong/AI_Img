from django.shortcuts import render

# Create your views here.
import json
from django.shortcuts import render, HttpResponse

from .models import Image
from .forms import GradeForm


def cmp(request, gid=None):
    # groups = Group.objects.all().order_by('name')
    # gid = gid or groups[0].id
    # group = Group.objects.get(id=gid)
    context = {'groups': groups, 'group': group}

    if request.method == 'POST':
        start = request.POST['start_time']
        end = request.POST['end_time']
        interval = request.POST['interval']
        # script, div = group.get_chart(start, end)
        # context = {'groups': groups, 'group': group}
        # context.update(dict(script=script, div=div))
        # context.update(dict(gid=gid, s=start, e=end))
        # return render(request, 'graph.html', context)
    return render(request, 'graph.html', context)


def grade(request):
    form = GradeForm
    context = {'form': form}
    return render(request, 'index.html', context)

