
from django.urls import path
from .views import *

urlpatterns = [
path("", index, name="home"),
path("on-boarding1/",on_boarding1, name="on-boarding1"), 
path("on-boarding2/",on_boarding2, name="on-boarding2"), 
path("on-boarding3/",on_boarding3, name="on-boarding3"),
path("on-boarding4/",on_boarding4, name="on-boarding4"), 
path("register-message/",register_message, name="register-message"),
path("payment-successfull/",payment_successfull, name="payment-successfull"), 
path("term-condition/", term_condition, name="term-condition"),
path("quiz-1/",quiz_1, name="quiz-1")
]
