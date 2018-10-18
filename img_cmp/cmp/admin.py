from django.contrib import admin
from .models import Image, Grade


# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'platform', 'version', 'resolution', 's3_url')
    search_fields = ('name', 'project')


class GradeAdmin(admin.ModelAdmin):
    list_display = ('img', 'date', 'comment', 'dem1', 'dem2', 'dem3', 'dem4', 'dem5')


admin.site.register(Image, ImageAdmin)
admin.site.register(Grade, GradeAdmin)
