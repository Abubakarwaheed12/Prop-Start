from django.contrib import admin
from courses.models import(
    Instructor,
    CourseCategory,
    Cousre,
    Lesson,
    Lectures,
    UserCourse
)
# Register your models here.

admin.site.register(Instructor)
admin.site.register(CourseCategory)
admin.site.register(Cousre)
# admin.site.register(Lesson)
# admin.site.register(Lectures)
admin.site.register(UserCourse)

class LecturesInline(admin.StackedInline):
    model = Lectures
    extra = 1  


@admin.register(Lesson)
class LessonInline(admin.ModelAdmin):  
    list_display = ('id', 'name', 'lesson_description', 'created_at', 'updated_at')
    inlines = [LecturesInline]


    
