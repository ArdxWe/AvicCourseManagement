from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Course(models.Model):
    course_name = models.CharField(max_length=20)
    course_scores = models.FloatField()
    teacher_name = models.CharField(max_length=20)
    semester = models.CharField(max_length=5, choices=(('1', '春'), ('2', '秋')))

    def __str__(self):
        if self.course_name:
            return str(self.course_name)
        else:
            return "None"


class Usercourse(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    scores = models.IntegerField(validators=[MaxValueValidator(100),
                                             MinValueValidator(0)
                                            ], null=True)
    
    class Meta:
        unique_together = ['user_name', 'course']

    def __str__(self):
        if self.user_name:
            return str(self.user_name) + ' ' + str(self.course)
        else:
            return "None"
