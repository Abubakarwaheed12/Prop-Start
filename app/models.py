from django.db import models

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
    email = models.EmailField(max_length=200, null=True, blank=True)

    what_Like_to_Learn = models.CharField(max_length=200, help_text='What Would you Like to Learn?', null=True, blank=True)

    is_nz_permanent = models.CharField(max_length=200, help_text='Are you Aus or NZ Permanent Resident?', null=True, blank=True)
    is_full_time = models.CharField(max_length=200, help_text='Do you work Full Time?', null=True, blank=True)
    is_saving_50k = models.CharField(max_length=200, help_text='Do you have savings of $50k or more?', null=True, blank=True)

    is_capcity_to_save = models.CharField(max_length=200, help_text='Do you have Capacity to Save?', null=True, blank=True)
    do_you_foresee_getting_a_FT_Job_in_next_6_years = models.CharField(max_length=200, help_text='Do you Foresee getting a FT Job in next 6 years?', null=True, blank=True)

    def __str__(self):
        return self.email or ""
