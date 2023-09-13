from django.urls import path
from .views import *

urlpatterns = [
    path("courses/",courses, name="courses"),
    path('checkout_session1/<int:course_id>', checkout_session1 , name="checkout_session1"),
    path("courses_payment_success/",courses_payment_success, name="courses_payment_success"),
    path("courses_payment_cancel/",courses_payment_cancel, name="courses_payment_cancel"),
    path("courses_form/<int:course_id>",course_form, name="courses_form"),
]