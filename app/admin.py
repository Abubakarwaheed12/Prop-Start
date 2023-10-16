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

# class CallAdmin(admin.ModelAdmin):
#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(is_paid=True)

# admin.site.register(BookingCall, CallAdmin)