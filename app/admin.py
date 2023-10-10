from django.contrib import admin
from .models import (
    BookingCall,
    TakeQuiz,
    PaymentHistory
)

# Register your models here.

admin.site.register(BookingCall)
admin.site.register(TakeQuiz)
admin.site.register(PaymentHistory)