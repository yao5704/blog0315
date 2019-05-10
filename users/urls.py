from django.contrib.auth.views import LoginView
from django.urls import path, include

from . import views
urlpatterns = [
    # 登录页面
    path('login/', views.login_view, name="login"),
    # 注销
    path('logout/', views.logout_view, name='logout'),
    # 注册页面
    path('register/', views.register, name='register'),
    #个人信息
    path('user_message/', views.user_message, name='user_message'),
    path('user_change/', views.user_change, name='user_change'),
]
app_name = 'users'