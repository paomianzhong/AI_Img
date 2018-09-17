from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('insert', views.insert, name='insert'),
    path('upload', views.upload, name='upload'),
    path('<str:project>/', views.compare, name='cmp'),
    path('grade/<int:pid>/', views.grade, name='grade'),
    path('api/export/', views.export, name='export'),
]
