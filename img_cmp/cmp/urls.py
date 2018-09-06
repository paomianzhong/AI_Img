from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:project>/', views.compare, name='cmp'),
    path('grade/<int:pid>/', views.grade, name='grade'),
]