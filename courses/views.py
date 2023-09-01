from django.shortcuts import render
from courses.models import(
    Instructor,
    CourseCategory,
    Cousre,
    Lesson,
    Lectures
)
# Create your views here.


def courses(request):
    courses = Cousre.objects.all().first()
    print(courses)
    context = {"course":courses}

    return render(request,"courses.html", context)
