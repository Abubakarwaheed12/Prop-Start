from django.db import models

# Create your models here.
class BookingCall(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)
    email = models.EmailField()
    state = models.CharField(max_length=255)
    is_resident = models.CharField(max_length=255)
    income = models.CharField(max_length=255)
    dependents = models.CharField(max_length=255)
    total_savings = models.CharField(max_length=255)
    total_home_loan = models.CharField(max_length=255)
    credit_card_limit = models.CharField(max_length=255)
    car_loan = models.CharField(max_length=255)
    other_loans = models.CharField(max_length=255)
    bad_credit_history = models.CharField(max_length=255)
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
