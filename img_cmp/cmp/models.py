# Create your models here.
from django.db import models


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
        pass

    def previous(self):
        pass

    @classmethod
    def category(cls):
        """
        获取图片的版本和分辨率种类
        :return:
        """
        versions = cls.objects.values("version")
        resolutions = cls.objects.values("resolution")
        ret = {'versions': set([v.get('version') for v in versions]),
               'resolutions': set([r.get('resolution') for r in resolutions])
               }
        return ret


class Grade(models.Model):
    img = models.ForeignKey(Image, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    dem1 = models.IntegerField(default=0)
    dem2 = models.IntegerField(default=0)
    dem3 = models.IntegerField(default=0)
    dem4 = models.IntegerField(default=0)
