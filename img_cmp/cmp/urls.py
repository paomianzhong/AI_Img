from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('insert', views.insert, name='insert'),
    path('upload', views.upload, name='upload'),
    path('cmp/<str:project>/', views.compare, name='cmp'),
    path('new/<str:project>/', views.compare2, name='compare2'),
    path('grade/<int:pid>/', views.grade, name='grade'),
    path('api/grade/<int:pid>/', views.grade2, name='grade2'),
    path('api/export/', views.export, name='export'),
]
