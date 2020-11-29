from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE


class College(models.Model):
    college_name = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.college_name)

class User(AbstractUser):   
    college = models.ForeignKey(College, on_delete=CASCADE, null=True)

    def __str__(self):
        return str(self.username)

class Course(models.Model):
    course_name = models.CharField(max_length=20)
    course_scores = models.FloatField()
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    teacher_name = models.CharField(max_length=20)
    semester = models.CharField(max_length=100, choices=(('spring', '春'), ('autumu', '秋')))
    description = models.TextField()


    def __str__(self):
        return str(self.course_name)


class Usercourse(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    scores = models.IntegerField(validators=[MaxValueValidator(100),
                                             MinValueValidator(0)
                                            ], null=True)
    
    class Meta:
        unique_together = ['user_name', 'course']

    def __str__(self):
        return str(self.user_name)


