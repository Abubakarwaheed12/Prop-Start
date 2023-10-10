from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(email, subject, message):
    
    from_email = settings.DEFAULT_FROM_EMAIL
    print('Send Email to the user')
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


def send_forget_password_mail(email, subject, message ):
    from_email = settings.DEFAULT_FROM_EMAIL
    print(from_email)
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return True