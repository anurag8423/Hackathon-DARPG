from django.urls import path
from Home import views
urlpatterns = [
    path('',views.home,name="home"),
    path('upload_audio/',views.upload_audio,name="upload_audio"),
    path('download/', views.download_file, name='download_file'),
    path('upload/',views.upload,name='upload'),                          
]