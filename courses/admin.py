from django.contrib import admin
from courses.models import(
    Instructor,
    CourseCategory,
    Cousre,
    Lesson,
    Lectures,
    premium_course
)

from .forms import (
    LectureForm,
    PremiumForm
)

# Register your models here.

admin.site.register(Instructor)
admin.site.register(CourseCategory)


class CourseModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if Cousre.objects.exists():
            return False
        return True


admin.site.register(Cousre, CourseModelAdmin)

class LecturesInline(admin.StackedInline):
    model = Lectures
    extra = 1  
    form = LectureForm
     

@admin.register(Lesson)
class LessonInline(admin.ModelAdmin):  
    list_display = ('id', 'name', 'lesson_description', 'created_at', 'updated_at')
    inlines = [LecturesInline]


    
@admin.register(premium_course)
class PremiumAdmin(admin.ModelAdmin):
    list_display=('id', 'name', 'lecture_description', 'created_at', 'updated_at')
    form = PremiumForm