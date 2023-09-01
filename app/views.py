from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login 


def index(request):
    return render(request,"index.html")
def courses(request):
    return render(request,"courses.html")
def quiz_1(request):
    return render(request,"take_quiz/quiz _1.html.")
def on_boarding1(request):
    return render(request,"book _a_call/on_boarding1.html.")
def on_boarding2(request):
    return render(request,"book _a_call/on_boarding2.html")
def on_boarding3(request):
    return render(request,"book _a_call/on_boarding3.html.")
def on_boarding4(request):
    return render(request,"book _a_call/on_boarding4.html.")
def register_message(request):
    return render(request,"book _a_call/register_message.html.")
def term_condition(request):
    return render(request,"term_condition.html")

