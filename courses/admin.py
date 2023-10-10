from django.contrib import admin
from courses.models import(
    Instructor,
    CourseCategory,
    Cousre,
    Lesson,
    Lectures,
    UserCourse,
    PreOrder,
)
# Register your models here.

admin.site.register(Instructor)
admin.site.register(CourseCategory)
admin.site.register(UserCourse)
admin.site.register(PreOrder)


class CourseModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if Cousre.objects.exists():
            return False
        return True


admin.site.register(Cousre, CourseModelAdmin)

class LecturesInline(admin.StackedInline):
    model = Lectures
    extra = 1  


@admin.register(Lesson)
class LessonInline(admin.ModelAdmin):  
    list_display = ('id', 'name', 'lesson_description', 'created_at', 'updated_at')
    inlines = [LecturesInline]


    
