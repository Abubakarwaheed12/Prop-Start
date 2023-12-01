from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import (
    BookingCall,
    TakeQuiz,
    Subscription,
    SubscriptionPlan,
)

# admin.site.register(BookingCall)
admin.site.register(TakeQuiz)
admin.site.register(Subscription)
admin.site.register(SubscriptionPlan)