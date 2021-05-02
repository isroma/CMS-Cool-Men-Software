from django.urls import path, re_path
from . import views

urlpatterns = [
    # path('upload', views.upload, name='upload'),
    # path('finalize', views.finalize, name='finalize'),
    path('upload/random_url/', views.tika, name='random_url'),
    re_path(r'^d/(?P<pk>.+?)$', views.download, name="download"),
    re_path(r'^finalize/(?P<prefix>.*?)$', views.finalize, name="finalize"),
    re_path(r'^upload/$', views.upload, name="upload"),
]