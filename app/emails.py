from django.core.mail import send_mail
from django.conf import settings
import threading 

def send_book_call_email(email):
    subject = "Schedule A Call"
    message = """
I hope this message finds you well. We're excited to connect with you and would like to schedule a call to discuss Course.

Your input and insights are valuable to us, and we believe that a conversation would be the best way to address any questions or concerns you may have.

Here are a few details to consider for our call:

Preferred Date and Time: Please let us know your availability for the call. We will do our best to accommodate your schedule.

Duration: The call is expected to last approximately 30min.

Meeting Platform: We can host the call on zoom , skype ,. If you have a preferred platform, please feel free to let us know.

To confirm the call and set the details, please reply to this email with your preferred date and time or any additional information you'd like to share. If you have any specific topics or questions you'd like to discuss during our call, please include those as well.

We're looking forward to a productive and engaging conversation. If you have any immediate questions or require further assistance before our scheduled call, please don't hesitate to reach out to us at [your contact information].

Thank you for your time, and we can't wait to connect with you!"""
    from_email = settings.EMAIL_HOST_USER
    print('Send Email to the user')
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)