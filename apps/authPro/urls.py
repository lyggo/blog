from django.urls import path
from . import views

app_name = 'authPro'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('graph-captcha/', views.graph_captcha, name='graph_captcha'),
    path('sms-captcha/', views.sms_captcha, name='sms_captcha'),
]