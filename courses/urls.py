from django.urls import path
from .views import *

urlpatterns = [
    path("courses/",courses, name="courses"),
]