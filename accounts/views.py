from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login 
from .models import CustomUser
from django.contrib.auth import logout
import threading
from .helpers import send_forget_password_mail
import random
# Create your views here.




def send_otp_email(email,otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    print(from_email)
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


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
            error_msg = "Password doesn't match. Try Again!"
            return render(request, "accounts/signup_page.html", {"error_msg":error_msg})
        elif CustomUser.objects.filter(email=email).exists():
            error_msg = "Username Already Exists"
            return render(request,"accounts/signup_page.html", {"error_msg":error_msg})
        else:
            # Start a new thread to send the email
            email_thread =threading.Thread(target=send_otp_email, args=(email,otp)) 
            email_thread.start()
            messages.success(request,"otp has been sent to your email")
            return redirect("send-code")
    return render(request,"accounts/signup_page.html")

def send_code(request):
    if request.method == "POST":
        otp_values = request.POST.getlist("code_number_input")
        print(otp_values)
        otp_ = "".join(otp_values)
        otp_int = int(otp_)
        print(otp_int)
        # otp = request.session["otp"]
        email = request.session["email"]
        password = request.session["password"]
        fname = request.session["fname"]
        lname = request.session["lname"]
        if otp_int:
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


def Login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        print(email,"login email")
        pass1 = request.POST.get("pass")
        print(pass1,"login pass")
        # remember_me = request.POST.get("remember_me") == "on"
        user = authenticate(request, email=email,password=pass1)
        print(user)
        if user is not None:
                login(request, user)
                # if remember_me:
                #     request.session.set_expiry(3600 * 24 * 30) 
                return redirect("home")
                # return render(request,"index.html")
        else:
            error_msg = "Invalid credentials"
            return render(request,"accounts/login_page.html", {"error_msg":error_msg})
    return render(request,"accounts/login_page.html")

def Logout(request):
    logout(request)
    return redirect("home")

def forget_password(request):
    otp = random.randint(1111,9999)
    print(otp,"forget pass")
    if request.method == "POST":
        email = request.POST.get("email")
        print(email)
        request.session['email_for_forget_password'] = email
        user_email = CustomUser.objects.filter(email=email)
        if user_email:
            email_thread = threading.Thread(target=send_forget_password_mail, args=(email,otp))
            email_thread.start()
            return redirect("forgot-password-code")
        else:
            error_message = "No user found with this email"
            return render(request,"accounts/forget_password.html", {"error_message":error_message})
        
    return render(request,"accounts/forget_password.html")

def enter_otp_for_forgot_password(request):
    if request.method == "POST":
        otp_values = request.POST.getlist("code_number_input")
        print(otp_values,"forgor password otp_value")
        email = request.session["email_for_forget_password"]
        otp_ = "".join(otp_values)
        otp_int = int(otp_)
        print(otp_int,"forgor password otp_int")
        if otp_int:
            user = CustomUser.objects.get(email=email)
            user.forget_password_token = otp_int
            user.save()
            # request.session.delete("email_for_forget_password")
            return redirect("reset-password")
        else:
            error_msg="Otp does not match"
            return render(request,"accounts/forgot_password_otp.html",{"error_msg":error_msg})
    return render(request,"accounts/forgot_password_otp.html")


def reset_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        print(password)
        new_password = request.POST.get("new-password")
        print (new_password)
        email = request.session["email_for_forget_password"]
        user = CustomUser.objects.get(email=email)
        if password != new_password:
            error_msg ="Passwords do not match"
            return render(request,"accounts/reset_password.html", {"error_msg": error_msg})
        elif new_password == user.password:     
            error_msg ="This password matches the old password.Try new password"
            return render(request,"accounts/reset_password.html", {"error_msg": error_msg})
        else:
            # success_message = "Password changes successfully"
            # return render(request,"accounts/reset_password", {"success_message":success_message})
            user.set_password(new_password)
            user.save()
            print(user.password)
            return redirect("password-success")
    return render(request,"accounts/reset_password.html")


def password_successfuly(request):
    return render(request,"accounts/password_successfully.html")

        






# def login(request):
#     return render(request,"book_a_call/on_boarding1.html")
# def login(request):
#     return render(request,"book_a_call/on_boarding2.html")
