
from django.urls import path
from .views import *

urlpatterns = [
path("", index, name="home"),
path("on-boarding1/",on_boarding1, name="on-boarding1"), 
path("on-boarding2/",on_boarding2, name="on-boarding2"), 
path("on-boarding3/",on_boarding3, name="on-boarding3"),
path("on-boarding4/",on_boarding4, name="on-boarding4"), 
# new add 
path("on_boarding5_date/",on_boarding5_date, name="on_boarding5_date"),
path("on_boarding_text/",on_boarding_text, name="on_boarding_text"),
# end 
path("register-message/",register_message, name="register-message"),
path("term_conditions/", term_conditions, name="term_conditions"),
path("privacy_policy/", privacy_policy, name="privacy_policy"),
path("website_disclaimer/", website_disclaimer, name="website_disclaimer"),
path("quiz-1/",quiz_1, name="quiz-1"),
path('checkout_session/', checkout_session , name="checkout_session"),
path('cancel/' , cancel , name="cancel"),
# paypal 
path('create_payment/',create_payment , name="create_payment"),
path('paypal_payment_successful/', paypal_payment_successful, name="paypal_payment_successful"),
# take_quiz
path('take_quiz/', take_quiz, name="take_quiz"),

]
