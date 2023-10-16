from django.shortcuts import render, redirect 
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login 
from django.http import JsonResponse, HttpResponse , HttpResponseNotFound
from .models import *
import stripe
from django.conf import settings
from django.urls import reverse 
from django.shortcuts import get_object_or_404
stripe.api_key =settings.STRIPE_PUBLIC_KEY
from paypalrestsdk import Payment 
import paypalrestsdk
import threading
from django.views.decorators.csrf import csrf_exempt
from .models import TakeQuiz , PaymentHistory
from .emails import(
    send_book_call_email,
    send_quiz_email,
    send_course_quiz_email
)


def index(request):

    return render(request,"index.html")


def quiz_1(request):
    return render(request, "quiz/quiz1.html")

def on_boarding1(request):
    
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        number = request.POST.get("number")
        print(fname, lname, email, number)
        booking_obj = BookingCall(
                first_name=fname,
                last_name=lname,
                contact_number= number,
                email=email)
        booking_obj.save()
        request.session["booking_id"]= booking_obj.id
        # messages.success(request, "Call booked successfully!")
        return redirect("on-boarding2")    
    return render(request,"bookcall/on_boarding1.html")
    

def on_boarding2(request):
    
    if request.method == "POST":
        state = request.POST.get("state")
        is_resident = request.POST.get("is_resident")
        income = request.POST.get("income")
        dependents = request.POST.get("dependents")
        # total_savings = request.POST.get("total_savings").replace("$" , "").replace(",", "")
        total_savings = request.POST.get("total_savings")
        total_home_loan = request.POST.get("total_home_loan")
        print(state,is_resident,income,dependents,total_savings,total_home_loan)
        if "yes" in request.POST:
            is_resident = True
        else:
            is_resident = False
        booking_obj_id = request.session.get("booking_id")
        booking_obj = BookingCall.objects.get(id=booking_obj_id)
        if booking_obj:
            booking_obj.state=state,
            booking_obj.is_resident = is_resident
            booking_obj.dependents = dependents
            booking_obj.income = income
            booking_obj.total_savings = total_savings
            booking_obj.total_home_loan = total_home_loan
            booking_obj.statedependents = dependents
            booking_obj.save()
            return redirect('on-boarding3')
        else:
            messages.error(request, "Booking information not found. Please start the booking process again.")
            return redirect('on-boarding1')
    return render(request,"bookcall/on_boarding2.html")
    

def on_boarding3(request):

    if request.method == "POST":
        credit_card_limit = request.POST.get("credit_card_limit")
        car_loan = request.POST.get("car_loan")
        other_loans = request.POST.get("other_loans")
        bad_credit_history = request.POST.get("bad_credit_history")
        agree_to_terms = request.POST.get("agree_to_terms")
        print(credit_card_limit, car_loan, other_loans,bad_credit_history, agree_to_terms)
        booking_obj_id = request.session["booking_id"]
        booking_obj = BookingCall.objects.get(id=booking_obj_id)

        booking_obj.credit_card_limit = credit_card_limit
        booking_obj.car_loan = car_loan
        booking_obj.other_loans = other_loans
        booking_obj.bad_credit_history = bad_credit_history
        booking_obj.save()
        return redirect('on-boarding4')
        
    return render(request, "bookcall/on_boarding3.html")
    

def on_boarding4(request):
    booking_obj_id = request.session["booking_id"]
    booking_obj = BookingCall.objects.get(id=booking_obj_id)
    context = {
        "booking_id": booking_obj.id
    }

    return render(request,"bookcall/on_boarding4.html", context)
   


# Stripe Checkout 
def checkout_session(request, booking_id = None):
    booking_obj_id = request.session["booking_id"]
    

    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
       
       line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                    'name': 'Invoice',
                    },
                    'unit_amount': 50 * 100 ,
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('register-message'))+ "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('cancel')),
    )


    print(checkout_session.id)

    print( 'Save Successfully')

    return redirect(checkout_session.url, code=303)


# Stripe  successfull payment
def register_message(request):

    session_id = request.GET.get('session_id')
    if session_id is None:
        return HttpResponseNotFound()
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    payment_id = session.payment_intent
    total_amount = session.amount_total / 100


    booking_obj_id = request.session["booking_id"]
    booking_obj = BookingCall.objects.get(id=booking_obj_id)
    booking_obj.is_paid = True
    booking_obj.pay_with = "stripe"
    booking_obj.payment_id = payment_id 
    booking_obj.save()
    PaymentHistory.objects.create(email=booking_obj.email, payment_purpose="Book Call", pay_with = "stripe", payment_id=payment_id, is_paid=True)
    email_thread = threading.Thread(target=send_book_call_email, args=(booking_obj.email, booking_obj.first_name, booking_obj.contact_number))
    email_thread.start()

    return render(request,"bookcall/register_message.html")

def cancel(request):
    return render(request,"bookcall/register_message.html")



# Paypal 
def create_payment(request, booking_id = None):
    booking_obj_id = request.session["booking_id"]

    price = 50
    full_host = request.get_host()
    schema = request.scheme

    paypal_client_id = settings.PAYPAL_CLIENT_ID
    paypal_client_secret = settings.PAYPAL_CLIENT_SECRET

    paypalrestsdk.configure({
        "mode": "sandbox",  # Use "live" for production
        "client_id": paypal_client_id,
        "client_secret": paypal_client_secret
    })

    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": f"{schema}://{full_host}/paypal_payment_successful/?amount={price}",
            "cancel_url": f"{schema}://{full_host}/cancel/"
        },
        "transactions": [{
            "amount": {
                "total": price,
                "currency": "USD"
            },
            "description": "Example Payment"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                return redirect(link.href)
    else:
        return render(request, 'bookcall/payment_cancelled.html')


# Paypal Payment Successfull 
def paypal_payment_successful(request):
    paymentid = request.GET.get('paymentId')

    amount = request.GET.get('amount')

    booking_obj_id = request.session["booking_id"]
    booking_obj = BookingCall.objects.get(id=booking_obj_id)
    booking_obj.is_paid = True
    booking_obj.pay_with = "stripe"
    booking_obj.payment_id = paymentid 
    booking_obj.save()
    PaymentHistory.objects.create(email=booking_obj.email, payment_purpose="Book Call", pay_with = "PayPal", payment_id=paymentid, is_paid=True)
    email_thread = threading.Thread(target=send_book_call_email, args=(booking_obj.email, booking_obj.first_name, booking_obj.contact_number))
    email_thread.start()

    return render(request, "bookcall/register_message.html")


# payment_cancelled 
def payment_cancelled(request):
    return render(request,"bookcall/payment_cancelled.html")

def term_conditions(request):
    return render(request,"term_conditions.html")

def privacy_policy(request):
    return render(request,"privacy_policy.html")

def website_disclaimer(request):
    return render(request,"website_disclaimer.html")

# new add 
def on_boarding5_date(request):
    return render(request, "bookcall/on_boarding5_date.html")

def on_boarding_text(request):
    return render(request, "bookcall/on_boarding_text.html")
# Function TO save Quiz Data
@csrf_exempt 
def take_quiz(request):
    if request.method =="POST":
        quiz = request.POST.dict()
        email = quiz.get('email')
        name = quiz.get('Your name')
        print(quiz)
        print(email, name)
        ans = ""
        for q , a in quiz.items():
            ans += f"Question :{q} \n\n"
            ans += f"Answer :{a} \n\n"
        take_quiz_obj = TakeQuiz.objects.create(quiz = ans, email=email)
        if quiz.get('Would you like to buy property one day in Australia?'):
            email_thread_2 = threading.Thread(target=send_course_quiz_email, args=(request, email, name))
            email_thread_2.start()
        else: 
            email_thread = threading.Thread(target=send_quiz_email, args=(request, email, name))
            email_thread.start()
        if take_quiz_obj:
            return JsonResponse({'response':'Quiz Added Successfully'})
        return JsonResponse({'error':'Error'})



