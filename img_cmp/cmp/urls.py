from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('grade/<int:pid>/', views.grade, name='grade'),
]