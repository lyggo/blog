from django.urls import path
from . import views

app_name = 'doc'

urlpatterns = [
    path('', views.index, name='index'),
    path('download-doc/', views.download_doc, name="download_doc"),
]