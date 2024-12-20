from django.urls import path
from video.views import VideoProcessView

urlpatterns = [
    path('api/video-process/', VideoProcessView.as_view(), name='video_process'),
    # Các đường dẫn khác
]
