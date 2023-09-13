from django.shortcuts import render,redirect 
from django.http import HttpResponseNotFound
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
    print (courses)
    
    context = {
        "course":courses,
        }
    if request.user.is_authenticated:
        usercourses=UserCourse.objects.filter(user=request.user, course=courses).exists()
        if usercourses:
            usercourse = UserCourse.objects.get(user=request.user, course=courses)
            context['usercourse'] = usercourse
    
    
    return render(request,"course/courses.html", context)

def course_form(request, course_id):
    context = {'course_id':course_id,}
    return render(request,'course/course_form.html' , context)


def checkout_session1(request , course_id):
    # host = request.get_host()
    course = get_object_or_404(Cousre, id= course_id)
    request.session["course_id"] = course_id

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

    return redirect(checkout_session.url, code=303)


def courses_payment_success(request):
    session_id = request.GET.get('session_id')
    if session_id is None:
        return HttpResponseNotFound()
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    payment_id = session.payment_intent
    total_amount = session.amount_total / 100

    course_id = request.session["course_id"]
    course_obj = Cousre.objects.get(id=course_id) 
    course_obj = UserCourse.objects.create(course=course_obj, user=request.user, is_paid = True)


    return render(request,"course/course_success_payment.html")



def courses_payment_cancel(request):
    return render(request,"course/course_cancel_payament.html")

