from django.urls import path
from .import views , detect
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns=[
    path('register',views.register,name='register'),
    path('index',TemplateView.as_view(template_name='index.html')),
    path('video_feed/', detect.video_feed, name='video_feed'),
    path('capture', views.capture, name='capture'),
    path('latestimage', views.serve_latest_image, name='latestimage'),
    path('picture', views.latest_picture, name='picture'),
    path('upload', views.uploadpicture, name='upload'),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
