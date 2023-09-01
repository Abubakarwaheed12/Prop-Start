from django.urls import path
from .views import *

urlpatterns = [
  path("login/", Login, name="login"),
  path("signup/", signup, name="signup"),
  path("send-code/",send_code,name="send-code"),
  path("forgot-password-code/",enter_otp_for_forgot_password,name="forgot-password-code"),
  path("forget-password/", forget_password, name="forget-password"),
  path("reset-password/",reset_password, name="reset-password"),
  path("password-success/",password_successfuly, name="password-success"),
  path("user_logout/", user_logout, name="user_logout"),
  
]
