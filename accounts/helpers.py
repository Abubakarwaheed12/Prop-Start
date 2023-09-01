from django.utils.crypto import get_random_string
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random

def send_forget_password_mail(email,otp):
    # token = get_random_string(length=4, allowed_chars='0123456789')
    # otp = random.randint(11111,99999)
    subject ="Your forgot password link"
    message=f"your otp is {otp}"
    from_email = settings.EMAIL_HOST_USER
    print(from_email)
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return True