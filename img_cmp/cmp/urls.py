from django.urls import path

from . import views
from . import api

urlpatterns = [
    path('', views.index, name='index'),
    path('up', views.up, name='up'),
    path('up1', views.up1, name='up1'),
    path('up2', views.up2, name='up2'),
    path('performance/<str:project>/', views.performance, name='performance'),
    path('chart/<str:project>/', views.chart, name='chart'),
    path('chart1/<str:project>/', views.chart1, name='chart1'),
    path('files/upload2/', views.fileupload, name='图片分片上传'),
    path('fileMerge/', views.fileMerge, name='上传成功合并'),
    path('cmp/<str:project>/', views.compare, name='cmp'),
    path('new/<str:project>/', views.compare2, name='compare2'),

    path('api/grade/<int:pid>/', api.grade, name='grade'),
    path('api/grade2/<int:pid>/', api.grade2, name='grade_detail'),
    path('api/insert', api.insert, name='insert'),
    path('api/insert1', api.insert1, name='insert1'),
    path('api/export/', api.export, name='export'),
    path('api/ssim/', api.get_ssim, name='ssim'),
    path('api/version/', views.update_version, name='version'),
    path('api/resolution/', views.update_resolution, name='resolution'),
]
