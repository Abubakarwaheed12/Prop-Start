import threading
import random
from django.shortcuts import render, redirect, HttpResponse
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login 
from django.contrib.auth import logout

from .models import CustomUser
from .emails import(
    send_otp_email,
    send_forget_password_mail
)
# Create your views here.


# Get all fields for signup and save in session till verify token 
def signup(request):
    if request.method == 'POST':
        firstname = request.POST.get("fname")
        lastname = request.POST.get("lname")
        email = request.POST.get("email")
        pass1 = request.POST.get("password")
        cpass = request.POST.get("cpass")
        otp = get_random_string(length=4, allowed_chars='0123456789')
        request.session["email"] = email
        request.session["password"] = pass1
        request.session["otp"] = otp
        request.session["fname"] = firstname
        request.session["lname"] = lastname
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
def send_code(request):
    """
    Function For Sending Verification Email
    """
    if request.method == "POST":
        otp_values = request.POST.getlist("code_number_input")
        print(otp_values)
        otp_ = "".join(otp_values)
        otp_int = ""
        if otp_:
            otp_int = int(otp_)
            print(otp_int)

        otp = request.session["otp"]
        email = request.session["email"]
        password = request.session["password"]
        fname = request.session["fname"]
        lname = request.session["lname"]
        if otp_ == otp:
            user = CustomUser(email=email,first_name=fname, last_name=lname)
            user.set_password(password)
            print(user)
            user.save()
            print(user)
            request.session.delete('otp')
            request.session.delete('email')
            request.session.delete('password')
            request.session.delete('fname')
            request.session.delete('lname')
            messages.success(request,"you are successfully registered")
            return redirect("login")
        else:
            messages.error(request, "otp does not match.Try again!")
            return redirect("send-code")
    return render(request,"accounts/send_code.html")


# Login User
def Login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        print(email,"login email")
        pass1 = request.POST.get("pass")
        print(pass1,"login pass")
        user = authenticate(request, email=email,password=pass1)
        print(user)
        if user is not None:
                login(request, user)
                return redirect("courses")
        else:
            messages.error(request,"Invalid credentials")
            return render(request, "accounts/login_page.html")
    return render(request,"accounts/login_page.html")


# Forgot Password 
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
def enter_otp_for_forgot_password(request):
    
    if request.method == "POST":
        otp_values = request.POST.getlist("code_number_input")
        print(otp_values,"forgor password otp_value")
        email = request.session["email_for_forget_password"]
        print(email)
        fotp = request.session["fotp"]
        otp_ = "".join(otp_values)
        otp_int = int(otp_)
        print(otp_int,"forgor password otp_int")
        if  fotp == otp_int :
            user = CustomUser.objects.get(email=email)
            user.forget_password_token = otp_int
            user.save()   
            return redirect("reset-password")
        else:
            print("else")
            messages.error(request,"Otp does not match")
            return render(request, "accounts/forgot_password_otp.html")
    
    return render(request,"accounts/forgot_password_otp.html")
    
# Reset Password 
def reset_password(request):
    try:
        if request.method == "POST":
            password = request.POST.get("password")
            print(password)
            new_password = request.POST.get("new-password")
            print (new_password)
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


def password_successfuly(request):
    return render(request,"accounts/password_successfully.html")


def user_logout(requset):
    logout(requset)
    return redirect('/accounts/login')