from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from accounts.models import CustomUser 

# Create your models here.
class BookingCall(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)
    email = models.EmailField()
    state = models.CharField(max_length=255, null=True, blank=True)
    is_resident = models.CharField(max_length=255, null=True, blank=True)
    income = models.CharField(max_length=255, null=True, blank=True)
    dependents = models.CharField(max_length=255, null=True, blank=True)
    total_savings = models.CharField(max_length=255, null=True, blank=True)
    total_home_loan = models.CharField(max_length=255, null=True, blank=True)
    credit_card_limit = models.CharField(max_length=255, null=True, blank=True)
    car_loan = models.CharField(max_length=255, null=True, blank=True)
    other_loans = models.CharField(max_length=255, null=True, blank=True)
    bad_credit_history = models.CharField(max_length=255, null=True, blank=True)
    meeting_date_time = models.DateTimeField(null=True, blank=True)

    pay_with = models.CharField(max_length=200, null=True, blank=True)
    payment_id = models.CharField(max_length=200, null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def calculate_booking_amount(self):
        # Example logic: Calculate the amount based on some fields
        booking_amount = (
            self.total_home_loan +
            self.credit_card_limit +
            self.car_loan -
            self.other_loans
        )
        return max(0, booking_amount)
    
    def __str__(self):
        return self.email or self.first_name



class TakeQuiz(models.Model):
    email = models.EmailField(null=True, blank=True)
    quiz = models.TextField(null=True, blank=True, help_text="Flow Of Quiz")

    def __str__(self):
        return self.email or '-'
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        




class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_plan_id = models.CharField(max_length=100, blank=True, null=True)
    paypal_plan_id = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}" or f"{self.id}"

class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)
    paypal_subscription_id = models.CharField(max_length=100, blank=True, null=True)
    is_sctive = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email}" or f"{self.id}"
    
   

    