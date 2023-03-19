from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('', views.index, name='index'),
    path('version/', views.version, name='version'),
    path('status/', views.status, name='status'),
    path('login/', views.login, name='login'),
    path('badges/all/', views.list_all_badges, name='list_all_badges'),
    ]
