from django.urls import path

from .views import Index, Dashboard, History, VideoAnalysis, LiveStream
from .views import (get_vehicle_counts, get_objects, get_images, get_image_objects, get_table_records,download_excel,delete_video,
                    get_multiline_chart_records, get_line_chart_records, get_bar_chart_records, get_first_frame, video_prediction)
from .upload_video_apis import (get_multiline_chart_records_uploads, get_line_chart_records_uploads, get_bar_chart_records_uploads)
# from django.conf.urls.static import static
# from django.conf import settings
# import socketio_handler

urlpatterns = [
    path('index', Index.as_view(), name='index'),
    path('dashboard/<str:site_name>/', Dashboard.as_view(), name='dashboard'),
    path('history', History.as_view(), name='history'),
    path('video_analysis', VideoAnalysis.as_view(), name='video_analysis'),
    path('live_stream', LiveStream.as_view(), name='live_stream'),

    # apis urls
    path('apis/get_objects', get_objects, name='get_objects'),
    path('apis/get_images', get_images, name='get_images'),
    path('apis/get_vehicle_counts', get_vehicle_counts, name='get_vehicle_counts'),
    path('apis/get_image_objects', get_image_objects, name='get_image_objects'),



    path('apis/get_table_records', get_table_records, name='get_table_records'),
    path('apis/get_multiline_chart_records', get_multiline_chart_records,
         name='get_multiline_chart_records'),
    path('apis/get_line_chart_records', get_line_chart_records,
         name='get_line_chart_records'),
    path('apis/get_bar_chart_records', get_bar_chart_records,
         name='get_bar_chart_records'),
    path('apis/get_first_frame', get_first_frame, name='get_first_frame'),
    path('apis/video_prediction', video_prediction, name='video_prediction'),
    path('apis/download_excel', download_excel, name='download_excel'),
     path('apis/delete_video', delete_video, name='delete_video'),

     path('apis/get_multiline_chart_records_uploads', get_multiline_chart_records_uploads,
         name='get_multiline_chart_records_uploads'),
    path('apis/get_line_chart_records_uploads', get_line_chart_records_uploads,
         name='get_line_chart_records_uploads'),
    path('apis/get_bar_chart_records_uploads', get_bar_chart_records_uploads,
         name='get_bar_chart_records_uploads'),
]

# urlpatterns += static('/socket.io/', document_root=os.path.join(settings.BASE_DIR, 'node_modules', 'socket.io-client', 'dist'))
