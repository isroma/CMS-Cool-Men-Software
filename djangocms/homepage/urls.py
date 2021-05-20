from django.urls import path, re_path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('homepage/tika/', views.tika, name='tika'),
    path('signature/', views.signature, name='signature'),
    re_path(r'^d/(?P<pk>.+?)$', views.download, name="download"),
    re_path(r'^finalize/(?P<prefix>.*?)/(?P<container>.*?)$', views.finalize, name="finalize"),
    re_path(r'^homepage/$', views.upload, name="upload"),
]