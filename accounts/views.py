import threading
import random
from django.shortcuts import render, redirect, HttpResponse
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login 
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .emails import(
    send_otp_email,
    send_forget_password_mail
)
from .forms import CustomUserUpdateForm
from .decorator import redirect_authenticated_user
from vendor.gclander.client import GoogleAPIClient
from app.models import BookingCall, PaymentHistory
from vendor.hubspot.client import APIClient as HubspotAPIClient
# Create your views here.


# Get all fields for signup and save in session till verify token 
@redirect_authenticated_user
def signup(request):

    if request.method == 'POST':
        firstname = request.POST.get("fname")
        lastname = request.POST.get("lname")
        email = request.POST.get("email")
        pass1 = request.POST.get("password")
        cpass = request.POST.get("cpass")
        phone = request.POST.get("number")
        print(type(phone))
        if len(str(phone)) > 15:
            messages.error(request,"Please enter correct number!")
            return redirect("signup")
        otp = get_random_string(length=4, allowed_chars='0123456789')
        request.session["email"] = email
        request.session["password"] = pass1
        request.session["otp"] = otp
        request.session["fname"] = firstname
        request.session["lname"] = lastname
        request.session["phone"] = phone
        
        if pass1!=cpass:
            messages.error(request,"Password doesn't match. Try Again!")
            return redirect("signup")
        elif CustomUser.objects.filter(email__iexact=email.lower()).exists():
            messages.error(request,"Username Already Exists")
            return redirect("signup")
        else:
            # Start a new thread to send the email
            subject = f"Registration OTP"
            message = f"Your Registration Token is {otp}"

            email_thread =threading.Thread(target=send_otp_email, args=(email, subject, message)) 
            email_thread.start()
            messages.success(request,"otp has been sent to your email")
            return redirect("send-code")
    return render(request,"accounts/signup_page.html")

# Send Registratin Verification Code
@redirect_authenticated_user
def send_code(request):
    """
    Function For Sending Verification Email
    """
    if request.method == "POST":
        otp_values = request.POST.getlist("code_number_input")
        print(otp_values)
        otp_ = "".join(otp_values)

        otp = request.session["otp"]
        email = request.session["email"]
        password = request.session["password"]
        fname = request.session["fname"]
        lname = request.session["lname"]
        phone = request.session["phone"]
        if otp_ == otp:
            user = CustomUser(email=email,first_name=fname, last_name=lname, phone_number=phone)
            user.set_password(password)
            user.save()
            # send to hubspot
            try:
                a = user.user_send_to_hubspot()
                print("Hubspot : ", a)
            except Exception as e:
                print(e, "User send to hubspot ends with error.")

            # Login User 
            user = authenticate(request, email=email,password=password)
            if user is not None:
                login(request, user)
                request.session.delete('otp')
                request.session.delete('email')
                request.session.delete('password')
                request.session.delete('fname')
                request.session.delete('lname')
                messages.success(request, "Thank you for registering your interest for the Property Pro course. We will notify you via email as soon as this course is ready!")
                return redirect('courses')
            messages.success(request,"you are successfully registered")
            return redirect("login")
        else:
            messages.error(request, "otp does not match.Try again!")
            return redirect("send-code")
    return render(request,"accounts/send_code.html")


# Login User
@redirect_authenticated_user
def Login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        pass1 = request.POST.get("pass")
        otp = get_random_string(length=4, allowed_chars='0123456789')
        request.session["otp"] = otp
        request.session["email"] = email
        request.session["password"] = pass1
        user = authenticate(request, email=email,password=pass1)
        if user is not None:
                # login(request, user)
                # Start a new thread to send the email
                subject = f"Login OTP"
                message = f"Your Login OTP is {otp}"
                email_thread =threading.Thread(target=send_otp_email, args=(email, subject, message)) 
                email_thread.start()
                messages.success(request,"otp has been sent to your email")
                return redirect("verify_login_otp")
        else:
            messages.error(request,"Invalid credentials")
            return render(request, "accounts/login_page.html")
    return render(request,"accounts/login_page.html")


# Login Otp Verification: 
@redirect_authenticated_user
def verify_login_otp(request):
    if request.method == "POST":
        otp_values = request.POST.getlist("code_number_input")
        print(otp_values)
        otp_ = "".join(otp_values)
        otp = request.session["otp"]
        pass1 = request.session["password"]
        email = request.session["email"]
        if otp_ == otp:
            user = authenticate(request, email=email,password=pass1)
            if user is not None:
                login(request, user)
                return redirect('courses')
            print(email, pass1)
        messages.error(request, 'Otp is not correct.')

    return render(request, 'accounts/login_otp.html')


# Forgot Password 
@redirect_authenticated_user
def forget_password(request):
    try:
        otp = random.randint(1111,9999)
        print(otp,"forget pass")
        request.session["fotp"] = otp
        if request.method == "POST":
            email = request.POST.get("email")
            print(email)
            request.session['email_for_forget_password'] = email
            user_email = CustomUser.objects.filter(email=email)
            if user_email:
                subject = "Forgot Password OTP"
                message = f"your forgot password OTP IS : {otp}"
                email_thread = threading.Thread(target=send_forget_password_mail, args=(email, subject, message))
                email_thread.start()
                messages.success(request,"Check the OTP code for password reset.")
                return redirect("forgot-password-code")
            else:
                messages.error(request,"No user found with this email")
                return redirect("forget-password")   
        return render(request,"accounts/forget_password.html")
    
    except Exception as e:
        print(e)

# for Password Token Verification
@redirect_authenticated_user 
def enter_otp_for_forgot_password(request):
    
    if request.method == "POST":
        otp_values = request.POST.getlist("code_number_input")
        email = request.session["email_for_forget_password"]
        fotp = request.session["fotp"]
        otp_ = "".join(otp_values)
        otp_int = int(otp_)
        if  fotp == otp_int :
            user = CustomUser.objects.get(email=email)
            user.forget_password_token = otp_int
            user.save()   
            return redirect("reset-password")
        else:
            messages.error(request,"Otp does not match")
            return render(request, "accounts/forgot_password_otp.html")
    
    return render(request,"accounts/forgot_password_otp.html")
    
# Reset Password 
@redirect_authenticated_user
def reset_password(request):
    try:
        if request.method == "POST":
            password = request.POST.get("password")
            new_password = request.POST.get("new-password")
            email = request.session["email_for_forget_password"]
            user = CustomUser.objects.get(email=email)
            if password != new_password:
                messages.success(request,"Both password does not match")
                return redirect("reset-password")
            elif password == user.password:  
                messages.error(request,"This password matches the old password.Try new password")
                return redirect("reset-password")   
            else:
                user.set_password(password)
                user.save()
                print(user.password)
                messages.success(request,"Password changed successfully")
                return redirect("password-success")
        return render(request,"accounts/reset_password.html")
    except Exception as e:
        print(e)

@redirect_authenticated_user
def password_successfuly(request):
    return render(request,"accounts/password_successfully.html")


def user_logout(requset):
    logout(requset)
    return redirect('/accounts/login')


# Change Password 
@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        cnew_password = request.POST.get('cnew_password')
        print(current_password, new_password, cnew_password)
        if new_password != cnew_password:
            messages.error(request, 'New password and confirm password should be same.')
            return redirect('change_password')
            
        if request.user.check_password(current_password):
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Password changed successfully.')
            
            login(request, request.user, backend='django.contrib.auth.backends.ModelBackend')
            
            return redirect('change_password')  
        else:
            messages.error(request, 'Invalid current password.')
    return render(request, 'accounts/change_password.html')


# Profile
@login_required
def profile(request):
    user = request.user
    calls =  BookingCall.objects.filter(email=user.email).order_by("-id")
    payments = PaymentHistory.objects.filter(email=user.email).order_by("-id")
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            messages.success(request, 'Profile Updated Successfully!')
            form.save()
            return redirect('profile')
    else:
        form = CustomUserUpdateForm(instance=user)
    
    context = {'form': form,'calls':calls, "payments":payments}
    return render(request, 'accounts/profile.html', context)
