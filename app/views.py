from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login 
from django.http import JsonResponse, HttpResponse
from .models import *
import stripe
from django.conf import settings
stripe_key = stripe.api_key =settings.STRIPE_PUBLIC_KEY 


def index(request):
    return render(request,"index.html")


def quiz_1(request):
    return render(request, "quiz/quiz_1.html")

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
        booking_obj = BookingCall.objects.get(id=booking_obj_id).first()
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

    # if request.method == "POST":
    #     credit_card_limit = request.POST.get("credit_card_limit")
    #     car_loan = request.POST.get("car_loan")
    #     other_loans = request.POST.get("other_loans")
    #     bad_credit_history = request.POST.get("bad_credit_history")
    #     agree_to_terms = request.POST.get("agree_to_terms")
    #     print(credit_card_limit, car_loan, other_loans,bad_credit_history, agree_to_terms)
    #     booking_obj_id = request.session["booking_id"]
    #     booking_obj = BookingCall.objects.get(id=booking_obj_id).first()
    #     if booking_obj:
    #         booking_obj.credit_card_limit = credit_card_limit
    #         booking_obj.car_loan = car_loan
    #         booking_obj.other_loans = other_loans
    #         booking_obj.bad_credit_history = bad_credit_history
    #         booking_obj.save()
    #         return redirect('on-boarding4')
    #     else:
    #         messages.error(request, "Booking information not found. Please start the booking process again.")
    #         return redirect('on-boarding1')    
    return render(request, "bookcall/on_boarding3.html")
    

def on_boarding4(request):
    
    return render(request,"bookcall/on_boarding4.html")
   





def register_message(request):
    return render(request,"bookcall/register_message.html")

def term_condition(request):
    return render(request,"term_condition.html")

# payment_successfull 
def payment_successfull(request):
    return render(request,"book_a_call/payment_successfull.html")

# payment_cancelled 

def payment_cancelled(request):
    return render(request,"bookcall/payment_cancelled.html")

