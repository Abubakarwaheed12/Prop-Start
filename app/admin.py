from django.contrib import admin
from .models import (
    BookingCall,
    TakeQuiz
)

# Register your models here.

admin.site.register(BookingCall)
admin.site.register(TakeQuiz)