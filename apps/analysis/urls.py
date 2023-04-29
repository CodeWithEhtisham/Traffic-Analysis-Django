from django.urls import path

from .views import Index,Dashboard,History,VideoAnalysis,LiveStream
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('index',Index.as_view() , name='index'),
    path('dashboard',Dashboard.as_view() , name='dashboard'),
    path('history',History.as_view() , name='history'),
    path('video_analysis',VideoAnalysis.as_view() , name='video_analysis'),
    path('live_stream',LiveStream.as_view() , name='live_stream'),
    # path('socket.io.js', socketio_js, name='socketio_js'),
    # path('video/', video_stream, name='video_stream'),
#     path('', Register.as_view(), name='register'),
]

urlpatterns += static('/socket.io/', document_root=os.path.join(settings.BASE_DIR, 'node_modules', 'socket.io-client', 'dist'))