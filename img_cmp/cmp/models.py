# Create your models here.
from django.db import models
from collections import defaultdict
from operator import itemgetter, add
from functools import reduce
from pandas import DataFrame
import arrow
import tablib


class Image(models.Model):
    name = models.CharField(max_length=64)
    project = models.CharField(max_length=64)
    platform = models.CharField(max_length=64, default='')
    version = models.CharField(max_length=64)
    resolution = models.CharField(max_length=64) # for some project this field represent category
    s3_url = models.CharField(max_length=4096)
    # ssim value compare to the origin image
    ssim = models.FloatField(default=0.0, blank=True, null=True)
    # vmaf value compare to the origin image
    vmaf = models.FloatField(default=0.0, blank=True, null=True)
    # if this image is improved over the previous version. 1: True, -1:False
    improved = models.IntegerField(default=0, blank=True, null=True)
    active = models.NullBooleanField(default=True, blank=True, null=True)

    def delete(self):
        self.active = False
        self.save()

    def get_improved(self):
        return self.improved >= 0

    def add_improved(self, mark):
        self.improved += mark
        self.save()

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
    def get_grades_avg(cls, proj, ver, reso):
        """
        获取图片平均分信息
        """
        imgs = Image.objects.filter(project=proj, version=ver, resolution=reso)
        rows = [Grade.get_average(img) for img in imgs]
        df = DataFrame(rows, index=[r.pop('version') for r in rows])
        df.loc['total'] = df.median()
        return df

    @classmethod
    def get_grades_detail(cls, proj, ver, reso):
        """
        获取图片打分历史信息
        """
        imgs = Image.objects.filter(project=proj, version=ver, resolution=reso)
        rows = [Grade.get_record(img) for img in imgs]
        df = DataFrame(rows, index=[img.name for img in imgs])
        return df

    @classmethod
    def export_xls(cls, proj, ver):
        """
        导出图片打分信息为xls文件
        :return:
        """
        total_imgs = Image.objects.filter(project=proj, version=ver)
        resolutions = set([r.get('resolution') for r in total_imgs.values("resolution")])
        data_set = set()
        total_headers = ['名称']
        total_stats = tablib.Dataset()
        total_stats.title = 'Total Average'
        for resolution in resolutions:
            imgs = Image.objects.filter(project=proj, version=ver, resolution=resolution)
            grade_times = [img.get_grade_times() for img in imgs]
            width = max(grade_times)
            stats = tablib.Dataset()
            aver_data = ['Average']
            headers = ['名称']
            new_col = []

            if proj == 'Mark':
                stats.title = ver
                getter = itemgetter('dem1', 'dem2', 'dem3', 'dem4')
                dem_list = ['对焦', '清晰', '曝光', '颜值']
            elif proj == 'Zhaidai_Project':
                stats.title = resolution
                getter = itemgetter('dem1', 'dem2', 'dem3', 'dem4', 'dem5')
                dem_list = ['对焦', '清晰', '曝光', '颜值', '纹理']
            elif proj == 'AI-case':
                stats.title = resolution
                getter = itemgetter('dem1', 'dem2', 'dem3', 'dem4', 'dem5')
                dem_list = ['振铃效应', '块效应', '噪声', '模糊', '失真']
            else:
                stats.title = resolution
                getter = itemgetter('dem1')
                dem_list = ['改进空间']

            for img in imgs:
                data = getter(img.get_stats(width=width))
                if isinstance(data, list):
                    data = (data,)
                dct = set(data[0])
                if dct == {''}:
                    continue
                row = reduce(add, data)
                row.insert(0, img.name)
                stats.append(row)

            for dem in dem_list:
                h = [dem + str(i) for i in (list(range(width)) + ['avg'])]
                headers.extend(h)
            stats.headers = headers
            for header in headers[1:]:
                if header.endswith('avg'):
                    h_list = list(filter(lambda x: x != '', stats[header]))
                    try:
                        aver_data.append(str(round(sum(h_list)/len(h_list), 2)))
                    except ZeroDivisionError:
                        aver_data.append(0)
                else:
                    aver_data.append('\\')
            stats.append(aver_data)

            for s in stats:
                data_col = []
                for index in range(len(stats.headers)):
                    if stats.headers[index].endswith('avg'):
                        data_col.append(float(s[index]))
                try:
                    new_col.append(str(round(sum(data_col)/len(data_col), 2)))
                except ZeroDivisionError:
                    new_col.append(0)
            stats.append_col(new_col, header='Average')
            dem_list.append('Average')

            data_set.add(stats)
            last_data = list(stats[-1])
            last_data[0] = resolution
            filter_aver_data = list(filter(lambda x: x != '\\', last_data))
            total_stats.append(filter_aver_data)

        total_headers.extend(dem_list)
        total_stats.headers = total_headers
        total_average = ['Total Average']
        for dem in dem_list:
            h_list = list(filter(lambda x: x != '', total_stats[dem]))
            total_list = [float(x) for x in h_list]
            try:
                total_average.append(str(round(sum(total_list)/len(total_list), 2)))
            except ZeroDivisionError:
                total_average.append(0)
        total_stats.append(total_average)
        data_set.add(total_stats)
        book = tablib.Databook(data_set)
        return book.export('xls')

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

    @classmethod
    def get_record(cls, img):
        getter = itemgetter('dem1','dem2','dem3','dem4','dem5')
        grades = Grade.objects.filter(img=img)
        stat = [getter(grade.__dict__) for grade in grades]
        return list(zip(*stat))

    @classmethod
    def get_average(cls, img, category=False, version=False):
        getter = itemgetter('dem1', 'dem2', 'dem3', 'dem4', 'dem5')
        if category:
            grades = Grade.objects.filter(img__project=img.project, img__version=img.version, img__resolution=img.resolution)
            stat = [getter(grade.__dict__) for grade in grades]
            return cls._calc_avg(img.resolution, stat)
        if version:
            grades = Grade.objects.filter(img__project=img.project, img__version=img.version)
            stat = [getter(grade.__dict__) for grade in grades]
            return cls._calc_avg(img.version, stat)
        grades = Grade.objects.filter(img=img)
        stat = [getter(grade.__dict__) for grade in grades]
        return cls._calc_avg(img.name, stat)

    @staticmethod
    def _calc_avg(ver, data):
        ret = {'version': ver}
        if not data:
            return ret
        header = ('dem1', 'dem2', 'dem3', 'dem4', 'dem5')
        df = DataFrame(data, columns=header)
        avg_dict = dict(zip(header, df.median().round(2)))
        ret.update(avg_dict)
        ret.update({'avg': round(df.median().mean(), 2)})
        return ret


class Performance(models.Model):
    project = models.CharField(max_length=64, default='')
    platform = models.CharField(max_length=64, default='')
    version = models.CharField(max_length=64, default='')
    resolution = models.CharField(max_length=64, default='')
    phone = models.CharField(max_length=64, default='')
    time_avg = models.FloatField(default=0)
    time_max = models.FloatField(default=0)
    cpu_avg = models.FloatField(default=0)
    cpu_max = models.FloatField(default=0)
    mem_avg = models.FloatField(default=0)
    mem_max = models.FloatField(default=0)

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
        phone = query_set.values("phone")
        ret = {'versions': set([v.get('version') for v in versions]),
               'resolutions': set([r.get('resolution') for r in resolutions]),
               'platforms': set([p.get('platform') for p in platforms]),
               'phone': set([ph.get('phone') for ph in phone])
               }
        return ret

    @classmethod
    def get_project(cls):
        projects = cls.objects.values("project")
        return set([p.get('project') for p in projects])

    @classmethod
    def get_platform(cls, project_name):
        query_set = cls.objects.filter(project=project_name)
        platforms = query_set.values("platform")
        return set([pl.get('platform') for pl in platforms])

    @classmethod
    def get_version(cls, project_name, platform_name=None):
        if platform_name:
            query_set = cls.objects.filter(project=project_name, platform=platform_name)
        else:
            query_set = cls.objects.filter(project=project_name)
        versions = query_set.values("version")
        return set([v.get('version') for v in versions])

    @classmethod
    def get_all_resolutions(cls):
        query_set = cls.objects.all().values('resolution')
        # resolutions = query_set.values("resolution")
        return set([r.get('resolution') for r in query_set])

    @classmethod
    def get_phone(cls, project_name, platform_name=None):
        if platform_name:
            query_set = cls.objects.filter(project=project_name, platform=platform_name)
        else:
            query_set = cls.objects.filter(project=project_name)
        phones = query_set.values("phone")
        return set([ph.get('phone') for ph in phones])



