from django.shortcuts import render,redirect
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse
from courses.models import(
    Instructor,
    CourseCategory,
    Cousre,
    Lesson,
    Lectures,
    UserCourse
)
# Create your views here.


def courses(request):
    courses = Cousre.objects.all().first()
    usercourse=UserCourse.objects.filter()
    context = {"course":courses}
    return render(request,"course/courses.html", context)

def courses_payment_success(request):
    return render(request,"course/course_success_payment.html")
    
def courses_payment_cancel(request):
    return render(request,"course/course_cancel_payament.html")

def checkout_session1(request , course_id):
    # host = request.get_host()
    course = get_object_or_404(Cousre, id= course_id)

    price = course.price
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
        success_url=request.build_absolute_uri(reverse('courses_payment_success'))+ "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('courses_payment_cancel')),
    )
     
    # invoice_obj.stripe_payment_intent = checkout_session.id
    # invoice_obj.save()

    print(checkout_session.id)

    print( 'Save Successfully')

    return redirect(checkout_session.url, code=303)

def course_form(request, course_id):
    context = {'course_id':course_id,}
    return render(request,'course/course_form.html' , context)