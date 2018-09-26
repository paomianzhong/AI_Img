# Create your models here.
from django.db import models
from collections import defaultdict
from operator import itemgetter, add
from functools import reduce
import arrow
import tablib


class Image(models.Model):
    name = models.CharField(max_length=64)
    project = models.CharField(max_length=64)
    platform = models.CharField(max_length=64, default='')
    version = models.CharField(max_length=64)
    resolution = models.CharField(max_length=64)
    s3_url = models.CharField(max_length=4096)

    def __str__(self):
        return self.name

    def next(self):
        img_id = self.id
        result = Image.objects.filter(pk__gt=img_id)
        return list(result)[0]

    def previous(self):
        img_id = self.id
        result = Image.objects.filter(pk__lt=img_id)
        return list(result)[-1]

    @classmethod
    def category(cls, project_name):
        """
        获取图片的版本和分辨率种类
        :return:
        """
        query_set = cls.objects.filter(project=project_name)
        versions = query_set.values("version")
        resolutions = query_set.values("resolution")
        platforms = query_set.values("platform")
        ret = {'versions': set([v.get('version') for v in versions]),
               'resolutions': set([r.get('resolution') for r in resolutions]),
               'platforms': set([p.get('platform') for p in platforms])
               }
        return ret

    @classmethod
    def get_project(cls):
        projects = cls.objects.values("project")
        return set([p.get('project') for p in projects])

    @classmethod
    def get_version(cls, project_name, platform_name=None):
        if platform_name:
            query_set = cls.objects.filter(project=project_name, platform=platform_name)
        else:
            query_set = cls.objects.filter(project=project_name)
        versions = query_set.values("version")
        return set([v.get('version') for v in versions])

    @classmethod
    def get_resolutions(cls, project_name, platform_name, version):
        query_set = cls.objects.filter(project=project_name, platform=platform_name, version=version)
        resolutions = query_set.values("resolution")
        return set([r.get('resolution') for r in resolutions])

    @classmethod
    def export_xls(cls, proj, ver):
        """
        导出图片打分信息为xls文件
        :return:
        """
        imgs = Image.objects.filter(project=proj, version=ver)

        grade_times = [img.get_grade_times() for img in imgs]
        width = max(grade_times)
        stats = tablib.Dataset()
        if proj == 'Mark':
            getter = itemgetter('dem1', 'dem2', 'dem3', 'dem4')
            for img in imgs:
                data = getter(img.get_stats(width=width))
                row = reduce(add, data)
                row.insert(0, img.name)
                stats.append(row)
            headers = ['名称']
            for dem in ['对焦', '清晰', '曝光', '颜值']:
                h = [dem+str(i) for i in (list(range(width))+['avg'])]
                headers.extend(h)
            stats.headers = headers
            return stats.export('xls')
        else:
            getter = itemgetter('dem1', 'dem2')
            for img in imgs:
                data = getter(img.get_stats(width=width))
                row = reduce(add, data)
                row.insert(0, img.name)
                stats.append(row)
            headers = ['名称']
            for dem in ['改进空间', '其他']:
                h = [dem + str(i) for i in (list(range(width)) + ['avg'])]
                headers.extend(h)
            stats.headers = headers
            return stats.export('xls')

    def get_grade_times(self):
        """
        获取图片打分的次数
        :return:
        """
        grades = Grade.objects.filter(img=self)
        return len(grades)

    def get_stats(self, width=0):
        """
        获取图片评分的统计信息
        :return:
        """
        stat = defaultdict(list)
        grades = Grade.objects.filter(img=self)
        for grade in grades:
            stat['dem1'].append(grade.dem1)
            stat['dem2'].append(grade.dem2)
            stat['dem3'].append(grade.dem3)
            stat['dem4'].append(grade.dem4)
            stat['dem5'].append(grade.dem5)
        for v in stat.values():
            avg = round(sum(v)/len(v), 2)
            v.extend(['']*(width-len(v)))
            v.append(avg)
        if not grades:
            stat['dem1'].extend(['']*(width+1))
            stat['dem2'].extend(['']*(width+1))
            stat['dem3'].extend(['']*(width+1))
            stat['dem4'].extend(['']*(width+1))
            stat['dem5'].extend(['']*(width+1))
        return stat


class Grade(models.Model):
    img = models.ForeignKey(Image, on_delete=models.CASCADE)
    date = models.DateTimeField(default=arrow.arrow.datetime.now())
    comment = models.CharField(max_length=256, default='')
    dem1 = models.IntegerField(default=0)
    dem2 = models.IntegerField(default=0)
    dem3 = models.IntegerField(default=0)
    dem4 = models.IntegerField(default=0)
    dem5 = models.IntegerField(default=0)

    def get_stats(self, img):
        stat = defaultdict(list)
        grades = Grade.objects.filter(img=img)
        for grade in grades:
            stat['dem1'].append(grade.dem1)
            stat['dem2'].append(grade.dem2)
            stat['dem3'].append(grade.dem3)
            stat['dem4'].append(grade.dem4)
            stat['dem5'].append(grade.dem5)
        for v in stat.values():
            avg = round(sum(v)/len(v), 2)
            v.append(avg)
        return stat



