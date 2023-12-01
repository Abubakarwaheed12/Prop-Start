from django.urls import path
from .views import *

urlpatterns = [
    path("courses/",courses, name="courses"),
    path('checkout_session1/', checkout_session1 , name="checkout_session1"),
    path("courses_payment_success/",courses_payment_success, name="courses_payment_success"),
    path("courses_payment_cancel/",courses_payment_cancel, name="courses_payment_cancel"),
    path("courses_form/",course_form, name="courses_form"),
    path('pre_order/', pre_order, name="pre_order"),
    path("on_boarding_pay/",on_boarding_pay, name="on_boarding_pay"),
    
    # paypal 
    path('paypal_create_payment/<int:course_id>/', paypal_create_payment, name='paypal_create_payment'),
    path('paypal_courses_payment_success/', paypal_courses_payment_success, name="paypal_courses_payment_success"),
]