from django.urls import path
from .views import *

urlpatterns = [
    path("courses/",courses, name="courses"),
    path('checkout_session1/', checkout_session1 , name="checkout_session1"),
    path("courses_payment_success/",courses_payment_success, name="courses_payment_success"),
    path("courses_payment_cancel/",courses_payment_cancel, name="courses_payment_cancel"),
    path("courses_form/",course_form, name="courses_form"),
    path('pre_order/', pre_order, name="pre_order"),
    path('course_promo_code/', course_promo_code, name="course_promo_code"),
    path('free_course/', free_course, name="free_course"),
    # paypal 
    path('paypal_create_payment/<int:course_id>/', paypal_create_payment, name='paypal_create_payment'),
    path('paypal_courses_payment_success/', paypal_courses_payment_success, name="paypal_courses_payment_success"),
    # pre-order payment 
    path("pre_order_paypal_create_payment/", pre_order_paypal_create_payment, name="pre_order_paypal_create_payment"),
    path("pre_order_papal_success/", pre_order_papal_success, name="pre_order_papal_success"),
    path("pre_order_stripe_checkout_session/", pre_order_stripe_checkout_session),
    path("pre_order_stripe_checkout_session_success/", pre_order_stripe_checkout_session_success, name="pre_order_stripe_checkout_session_success"),
]