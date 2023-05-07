from django.urls import path

from .views import Index,Dashboard,History,VideoAnalysis,LiveStream
from .views import get_vehicle_counts,get_objects, get_images,get_image_objects
# from django.conf.urls.static import static
# from django.conf import settings
# import socketio_handler

urlpatterns = [
    path('index',Index.as_view() , name='index'),
    path('dashboard',Dashboard.as_view() , name='dashboard'),
    path('history',History.as_view() , name='history'),
    path('video_analysis',VideoAnalysis.as_view() , name='video_analysis'),
    path('live_stream',LiveStream.as_view() , name='live_stream'),
    
    # apis urls
    path('apis/get_objects',get_objects , name='get_objects'),
    path('apis/get_images',get_images , name='get_images'),
    path('apis/get_vehicle_counts',get_vehicle_counts , name='get_vehicle_counts'),
    path('apis/get_image_objects',get_image_objects , name='get_image_objects'),
]

# urlpatterns += static('/socket.io/', document_root=os.path.join(settings.BASE_DIR, 'node_modules', 'socket.io-client', 'dist'))