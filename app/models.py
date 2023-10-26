from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

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
        



class PaymentHistory(models.Model):
    email = models.CharField(max_length=200, null=True, blank=True)
    payment_purpose = models.CharField(max_length=200, null=True, blank=True)
    pay_with = models.CharField(max_length=200, null=True, blank=True)
    payment_id = models.CharField(max_length=200, null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self) :
        return self.payment_purpose or self.pay_with 
    

class PromoCode(models.Model):
    promo_code = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(8)],
        help_text="The value must be at least 8 characters long."
    )
    is_expired = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.promo_code or f"code-{self.id}"




class FullDiscountPromoCode(models.Model):
    promo_code = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(8)],
        help_text="The value must be at least 8 characters long."
    )
    is_expired = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Full Discount Code -{self.promo_code}"
 
    