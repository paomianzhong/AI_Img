from django.contrib import admin
from .models import Image

# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'platform', 'version', 'resolution', 's3_url')

admin.site.register(Image, ImageAdmin)
