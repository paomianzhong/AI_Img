# Create your models here.
from django.db import models
import arrow


class Image(models.Model):
    name = models.CharField(max_length=64)
    project = models.CharField(max_length=64)
    platform = models.CharField(max_length=64)
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
        ret = {'versions': set([v.get('version') for v in versions]),
               'resolutions': set([r.get('resolution') for r in resolutions])
               }
        return ret


class Grade(models.Model):
    img = models.ForeignKey(Image, on_delete=models.CASCADE)
    date = models.DateTimeField(default=arrow.arrow.datetime.now())
    comment = models.CharField(max_length=256, default='')
    dem1 = models.IntegerField(default=0)
    dem2 = models.IntegerField(default=0)
    dem3 = models.IntegerField(default=0)
    dem4 = models.IntegerField(default=0)
    dem5 = models.IntegerField(default=0)
