from django.urls import path

from . import views

urlpatterns = [
    path('', views.files, name='files'),
    path('<int:id>/', views.download, name='filesDownload'),
]
