from django.urls import path
from . import views

app_name = 'course'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:course_id>/', views.detail, name='detail'),
    path('token/', views.course_token, name='course_token'),
]