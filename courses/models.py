from django.db import models
from accounts.models import CustomUser
# Create your models here.

class Instructor(models.Model):
    name = models.CharField(max_length=200, help_text="Enter the Instructor Name.", null=True , blank=True )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.name or ''

    class Meta:
        ordering = ['-id']
        verbose_name = "Instructor"       
        verbose_name_plural = "Instructors"

    @classmethod
    def get_instructor_by_id(ins, instructor_id):
        try:
            return ins.objects.get(id=instructor_id)
        except ins.DoesNotExist:
            return None


class CourseCategory(models.Model):
    name =  models.CharField(max_length=200, help_text="Enter the Course Name.",)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.name or ''

    class Meta:
        ordering = ['-id']
        verbose_name = "Course Category"       
        verbose_name_plural = "Course Categories"


class Cousre(models.Model):
    instructor = models.ForeignKey(Instructor , on_delete=models.SET_NULL, null=True, blank=True , related_name="courses")
    name =  models.CharField(max_length=200, help_text="Enter the Course Name.",)
    course_description = models.TextField(null=True , blank=True)
    course_legth = models.CharField(max_length=200)
    category = models.ForeignKey(CourseCategory , on_delete=models.CASCADE, related_name="courses" )
    price = models.IntegerField(default=0 , null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.name or ''

    class Meta:
        ordering = ['-id']
        verbose_name = "Course"       
        verbose_name_plural = "Courses"


class Lesson(models.Model):
    course = models.ForeignKey(Cousre , on_delete=models.CASCADE, related_name="lessons")
    name =  models.CharField(max_length=200, help_text="Enter the Lesson Name.",)
    lesson_description = models.TextField(null=True , blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.name or ''

    class Meta:
        ordering = ['-id']
        verbose_name = "Lesson"       
        verbose_name_plural = "Lesson"



class Lectures(models.Model):
    lesson = models.ForeignKey(Lesson , on_delete=models.CASCADE, related_name="lectures")
    name =  models.CharField(max_length=200, help_text="Enter the Lecture Name.",)
    lecure_description = models.TextField(null=True , blank=True)
    video_url = models.URLField(null=True, blank=True)
    video = models.FileField(upload_to="lectures",help_text="please upload the lecture vide!")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.name or ''

    class Meta:
        ordering = ['-id']
        verbose_name = "Lecture"       
        verbose_name_plural = "Lectures"


class UserCourse(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Cousre, on_delete=models.SET_NULL, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    pay_with = models.CharField(max_length=200, null=True, blank=True)
    payment = models.CharField(max_length=200, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return f'{self.user.email}' or ''
    
    class Meta:
        ordering = ['-id']
        verbose_name = "User Course"       
        verbose_name_plural = "User Courses"



class PreOrder(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    pay_with = models.CharField(max_length=200, null=True, blank=True)
    payment = models.CharField(max_length=200, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return f'{self.user.email}' or ''
    
    class Meta:
        ordering = ['-id']
        verbose_name = "Pre Order"       
        verbose_name_plural = "Pre Orders"