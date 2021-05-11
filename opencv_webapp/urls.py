from django.urls import path
from . import views
from django.conf import settings
# settings.py에 쓰인 코드가 django.conf의 더 큰 settings.py로 들어감
from django.conf.urls.static import static

app_name = 'opencv_webapp'

urlpatterns = [
    path('', views.first_view, name='first_view'),
    # ''경로로 들어가면 opencv_webapp의 하위 views.py의 first_view함수에 의해 보여지는 html 결정
    path('simple_upload/', views.simple_upload, name='simple_upload'),
    path('detect_face/', views.detect_face, name='detect_face'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
