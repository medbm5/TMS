from django.urls import path

from . import views
app_name='myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='reslts'),
    path('upload_csv/', views.profile_upload, name='profile_upload'),


]