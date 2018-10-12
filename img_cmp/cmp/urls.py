from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('insert', views.insert, name='insert'),
    path('up', views.up, name='up'),
    path('up1', views.up1, name='up1'),
    path('performance/<str:project>/', views.performance, name='performance'),
    path('chart/<str:project>/', views.chart, name='chart'),
    path('chart1/<str:project>/', views.chart1, name='chart1'),
    path('files/upload2/', views.fileupload, name='图片分片上传'),
    path('fileMerge/', views.fileMerge, name='上传成功合并'),
    path('cmp/<str:project>/', views.compare, name='cmp'),
    path('new/<str:project>/', views.compare2, name='compare2'),
    path('grade/<int:pid>/', views.grade, name='grade'),
    path('api/grade/<int:pid>/', views.grade2, name='grade2'),
    path('api/export/', views.export, name='export'),
    path('api/version/', views.update_version, name='version'),
    path('api/resolution/', views.update_resolution, name='resolution'),
]
