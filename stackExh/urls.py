from django.urls import path
from . import views

urlpatterns = [
    path('', views.qform, name='qform'),
    path('answers/', views.answers, name='answers'),
    path('del/', views.delsession, name='delsession')
]