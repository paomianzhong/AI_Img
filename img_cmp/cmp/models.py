# Create your models here.
from django.db import models


class Image(models.Model):
    name = models.CharField(max_length=64)
    project = models.CharField(max_length=64)
    platform = models.CharField(max_length=64)
    version = models.CharField(max_length=64)
    s3_url = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Grade(models.Model):
    img = models.ForeignKey(Image, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    dem1 = models.IntegerField(default=0)
    dem2 = models.IntegerField(default=0)
    dem3 = models.IntegerField(default=0)
    dem4 = models.IntegerField(default=0)
