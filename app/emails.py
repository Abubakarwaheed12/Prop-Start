from django.core.mail import send_mail
from django.conf import settings
import threading 


# On Book Call
def send_book_call_email(email, name, phone, meeting_date_time):
    subject = "Schedule A Call"
    message = f"""
Hey {name},

This is a confirmation email for your Strategy Call.

We will reach out to you on {phone}  on {meeting_date_time}, please make yourself available for the call.

I want to take a moment to answer the most frequently asked questions:

    1) What if I miss the call? Your Strategist will be available for a call back, 10 minutes following your scheduled call time and will attempt to reach you 3 times during this window.
    2) What if I need to re-schedule? Please email info@propstart.com.au as soon as possible. All reschedules are subject to availability.
    3) Does my partner need to attend? Not for the initial call.
    4) What if I need to change my number? Please email info@propstart.com.au as soon as possible.
    5) What information should I have prepared? A basic understanding of your financials such as income and current loans.

If there are any other questions that you have, feel free to email info@propstart.com.au.

Excited to meet you!

The PropStart Team"""
    from_email = settings.DEFAULT_FROM_EMAIL
    print('Send Email to the user')
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


# Email for strategy session - quiz results
def send_quiz_email(request, email, name):
    subject = "Check your results: Is PropStart right for you?"
    book_call_url = f"{request.get_host()}/on-boarding1/"
    message = (f"""
Dear {name},

Your recent completion of our quiz, "Is PropStart Right for you?" has revealed some exciting opportunities for your growth, and we're eager to assist you in achieving your goals.

Based on your quiz responses, we're thrilled to inform you that you qualify for an exclusive 1 on 1 Strategy Session with one of our seasoned strategists at PropStart. This personalised session will provide you with invaluable insights tailored to your unique aspirations and challenges.

Here's what you can expect from your strategy call:

Personalised Guidance: Our experienced strategist will delve into your specific goals and circumstances to discover the right pathway forward for you

Expert Insights: Gain insights from professionals who have achieved success in the real estate field. Leverage their knowledge and expertise to make informed decisions

Q&A Opportunity: Have all your burning questions answered and gather valuable information to make well-informed decisions

To schedule your personalised strategy call, simply click on the link below, provide your details and choose a convenient time slot that works for you:

{book_call_url}

Thank you for considering PropStart as your partner on your journey to real estate success. We look forward to speaking with you during your strategy call and helping you reach new heights in the world of property.

Best regards,

The PropStart Team

""")
    from_email = settings.DEFAULT_FROM_EMAIL
    print('Send Email to the user')
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)



# Email for course - quiz results
def send_course_quiz_email(request, email, name):
    subject = "Check your results: Is PropStart right for you?"
    register_url = f"{request.get_host()}/accounts/signup/"
    message = (f"""
Dear {name},

Thank you for taking the time to complete our recent quiz, "Is PropStart right for you?". We're excited to share your results with you and provide valuable insights that can help you achieve your goals.

Based on your quiz responses, it's clear that you have a strong interest in the world of real estate. We're thrilled to inform you that PropStart's Online Property Course (Property Pro) is the perfect resource to help you take that next step towards success. 

We’re preparing this course for you now and will send you an email once we’re up and running. Make sure you register your details so that you’re notified as soon as we’re live

{register_url}

Here's how our course can benefit you:

Comprehensive Learning: Our course offers a comprehensive curriculum covering all aspects of the real estate industry

Flexible Learning: With our online platform, you can learn at your own pace, making it easy to balance your studies with your existing commitments.

Expert Instructors: Learn from seasoned real estate professionals who have successfully navigated the industry. Gain insights from their experiences and benefit from their expertise.

Thank you for choosing PropStart to be a part of your real estate journey. We look forward to helping you realise your full potential and seeing you succeed in the dynamic world of property.

Best regards,

The PropStart Team


""")
    from_email = settings.DEFAULT_FROM_EMAIL
    print('Send Email to the user')
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)



# Course Confirmation Email 
def course_confirmation_email(request):
    subject = "Course Confirmation"
    course_page_url = f"{request.get_host()}/courses/"
    name = request.user.first_name
    email = request.user.email
    message = (f"""Hey {name},

You've made a fantastic decision investing in yourself through registering for the Property Genius Unlocked course.

Access the course here - {course_page_url}

You have lifetime access to the Property Genius Unlocked course. It is simply designed in a digestible format to make the learning experience seamless and straight forward. With that in mind you can go as fast or slow as you'd like. ALSO, we do recommend going through the program multiple times to truly master this information.

If you have any technical issues or are unable to access the course, please email info@prostart.com.au so we can take care of you :)

Happy learning

The PropStart Team""")
    from_email = settings.DEFAULT_FROM_EMAIL
    print('Send Email to the user')
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)