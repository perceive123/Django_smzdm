from django.urls import path#, re_path
from . import views

urlpatterns = [
    # re_path(r'shorts?q=(?P<q>\w+)',views.shorts_q),
    path('index', views.phone_index),
    path('phone', views.phone_shorts),
    # 用户登录url
    # path('login', account.Login.as_view, name="login"),
    # 验证码url
    # path('get_auth_img', account.GetAuthImg.as_view, name="get_auth_img"),
    # 用户注册url
    # path('register', account.Register.as_view(), name="register"),
]