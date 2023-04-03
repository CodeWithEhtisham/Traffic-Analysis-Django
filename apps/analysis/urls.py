from django.urls import path

from .views import Index,Dashboard,History,VideoAnalysis,LiveStream,video_stream


urlpatterns = [
    path('index',Index.as_view() , name='index'),
    path('dashboard',Dashboard.as_view() , name='dashboard'),
    path('history',History.as_view() , name='history'),
    path('video_analysis',VideoAnalysis.as_view() , name='video_analysis'),
    path('live_stream',LiveStream.as_view() , name='live_stream'),
    path('video/', video_stream, name='video_stream'),
#     path('', Register.as_view(), name='register'),
]