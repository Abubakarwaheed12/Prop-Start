from django.shortcuts import render,redirect 
from django.http import HttpResponseNotFound
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import paypalrestsdk
from paypalrestsdk import Payment 
import threading
from django.contrib import messages
from courses.models import(
    Cousre,
)
from app.emails import(
    course_confirmation_email
)
from app.utils import send_to_hubspot
# Create your views here.


def courses(request):
    courses = Cousre.objects.all().last()
    context = {
        "course":courses,
        }
    
    
    return render(request,"course/courses.html", context)




def course_form(request):
    return render(request,'course/course_form.html')


def checkout_session1(request):
#     # host = request.get_host()

#     course = get_object_or_404(Cousre, id= course_id)
#     request.session["course_id"] = course_id
#     price = int(request.POST.get("total_price"))
    
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     checkout_session = stripe.checkout.Session.create(
       
#        line_items=[
#             {
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {
#                     'name': 'Invoice',
#                     },
#                     'unit_amount': int(price) * 100 ,
#                 },
#                 'quantity': 1,
#             }
#         ],
#         mode='payment',
#         success_url=request.build_absolute_uri(reverse('courses_payment_success'))+ "?session_id={CHECKOUT_SESSION_ID}",
#         cancel_url=request.build_absolute_uri(reverse('courses_payment_cancel')),
#     )
    # return redirect(checkout_session.url, code=303)
    
    user = request.user
    price_id="price_1O9ARLBeBXpxCROJrEDoMYV9"
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        payment_method_id = request.POST.get('payment_method_id')

        print("payment_method_id", payment_method_id)
        if user.stripe_customer_id:
            customer_id = user.stripe_customer_id
            stripe.PaymentMethod.attach(
                    payment_method_id,
                    customer=user.stripe_customer_id,
                )
        else:
            customer = stripe.Customer.create(
                email=user.email,
                name=user.first_name,
                payment_method=payment_method_id,
                invoice_settings={'default_payment_method': payment_method_id},
                
            )
            customer_id = customer.id
            user.stripe_customer_id = customer_id
            user.save()

        current_subscription_id = user.current_subscription

        if current_subscription_id:
            print("current subscription delete")
            subscription = stripe.Subscription.retrieve(current_subscription_id)
            subscription.delete(prorate=False)
        
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{"price": price_id}],
            expand=['latest_invoice.payment_intent'],
        )

        user.current_subscription = subscription.id
        user.save()

        return JsonResponse({"success":f"Subsciption is created Successfully!{subscription}"})



def courses_payment_success(request):
    # session_id = request.GET.get('session_id')
    # if session_id is None:
    #     return HttpResponseNotFound()
    # stripe.api_key = settings.STRIPE_SECRET_KEY
    # session = stripe.checkout.Session.retrieve(session_id)
    # payment_id = session.payment_intent
    # total_amount = session.amount_total / 100

    # course_id = request.session["course_id"]
    # course_obj = Cousre.objects.get(id=course_id) 
    # course_obj = UserCourse.objects.create(course=course_obj, user=request.user, is_paid = True, payment=payment_id, pay_with='Stripe')
    # request.session.delete("course_id")

    ethread = threading.Thread(target=course_confirmation_email, args=(request,))
    ethread.start()

    # send to hubspot
    user = request.user
    playload = {
    "fname" : f"{user.first_name}",
    "lname" : f"{user.last_name}",
    "email" : f"{user.email}",
    "phone" : f"{user.phone_number}",
    "lead_status" : "New course",
    }
    try:
        send_to_hubspot(**playload)
    except Exception as e:
        print(e)

    return render(request,"course/course_success_payment.html")



# Paypal 
def paypal_create_payment(request, course_id = None):
    
    course = get_object_or_404(Cousre, id= course_id)
    request.session["course_id"] = course_id
    price = int(request.POST.get("ptotal_price"))
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
            "return_url": f"{schema}://{full_host}/paypal_courses_payment_success/?amount={price}",
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
        return render(request, 'course/course_cancel_payament.html')

# Payment successful
def paypal_courses_payment_success(request):

    paymentid = request.GET.get('paymentId')
    amount = request.GET.get('amount')

    course_id = request.session["course_id"]
    course_obj = Cousre.objects.get(id=course_id) 
    
    ethread = threading.Thread(target=course_confirmation_email, args=(request,))
    ethread.start()
    # send to hubspot
    user = request.user
    playload = {
    "fname" : f"{user.first_name}",
    "lname" : f"{user.last_name}",
    "email" : f"{user.email}",
    "phone" : f"{user.phone_number}",
    "lead_status" : "New course",
    }
    try:
        send_to_hubspot(**playload)
    except Exception as e:
        print(e)
        
    return render(request,"course/course_success_payment.html")

def courses_payment_cancel(request):
    return render(request,"course/course_cancel_payament.html")

# Pre Order 
def pre_order(request):
    context = {
    }
    return render(request, 'course/pre_order.html', context)

# Paypal Pre Order
def pre_order_paypal_create_payment(request, ):

    price = 375 
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
            "return_url": f"{schema}://{full_host}/pre_order_papal_success/?amount={price}",
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
        return render(request, 'course/course_cancel_payament.html')
    
def pre_order_papal_success(request):
    paymentid = request.GET.get('paymentId')
    amount = request.GET.get('amount')
    # send to hubspot
    user = request.user
    playload = {
    "fname" : f"{user.first_name}",
    "lname" : f"{user.last_name}",
    "email" : f"{user.email}",
    "phone" : f"{user.phone_number}",
    "lead_status" : "New course",
    }
    try:
        send_to_hubspot(**playload)
    except Exception as e:
        print(e)
    return redirect('/')

def pre_order_stripe_checkout_session(request):
    price = 375
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
       
       line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                    'name': 'Invoice',
                    },
                    'unit_amount': int(price) * 100 ,
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('pre_order_stripe_checkout_session_success'))+ "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('courses_payment_cancel')),
    )

    return redirect(checkout_session.url, code=303)

def pre_order_stripe_checkout_session_success(request):
    session_id = request.GET.get('session_id')
    if session_id is None:
        return HttpResponseNotFound()
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    payment_id = session.payment_intent
    # send to hubspot
    user = request.user
    playload = {
    "fname" : f"{user.first_name}",
    "lname" : f"{user.last_name}",
    "email" : f"{user.email}",
    "phone" : f"{user.phone_number}",
    "lead_status" : "New course",
    }
    try:
        send_to_hubspot(**playload)
    except Exception as e:
        print(e)
    return redirect('/')



