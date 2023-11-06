
from django.shortcuts import render, redirect
import stripe
from .models import UserProfile

def manage_subscription(request, price_id="prod_Ox4Xez1WSY83tp"):
    user = request.user
    

    if user.stripe_customer_id:
        customer_id = user.stripe_customer_id
    else:
        customer = stripe.Customer.create(
            email=user.email,
        )
        customer_id = customer.id
        user.stripe_customer_id = customer_id
        user.save()

    current_subscription_id = user.current_subscription

    if current_subscription_id:
        subscription = stripe.Subscription.retrieve(current_subscription_id)
        subscription.items.create(
            price=price_id,
        )
    else:
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{"price": price_id}],
        )

    user.current_subscription = subscription.id
    user.save()

    return redirect('courses_payment_success')
