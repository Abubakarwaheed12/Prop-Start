from django.contrib import admin
from courses.models import(
    Instructor,
    CourseCategory,
    Cousre,
    Lesson,
    Lectures
)
# Register your models here.

admin.site.register(Instructor)
admin.site.register(CourseCategory)
admin.site.register(Cousre)
admin.site.register(Lesson)
admin.site.register(Lectures)
