from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('', views.index, name='index'),
    path('version/', views.version, name='version'),
    path('status/', views.status, name='status'),
    path('login/', views.login, name='login'),
    path('score/', views.score),
    path('badges/all/', views.list_all_achievements),
    path('badges/owned/', views.list_owned_badges),
    path('exercise/<slug:name>/', views.exercise_detail),
    path('submit/', views.submit),
    ]
