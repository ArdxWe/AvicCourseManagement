from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE


class College(models.Model):
    college_name = models.CharField(max_length=100, verbose_name="学院名")

    class Meta:
        verbose_name = '学院'
        verbose_name_plural = '学院'

    def __str__(self):
        return str(self.college_name)


class User(AbstractUser):
    college = models.ForeignKey(College, on_delete=CASCADE, null=True, verbose_name="所属学院")

    class Meta:
        ordering = ['username']
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return str(self.username)


class Course(models.Model):
    course_name = models.CharField(max_length=40, verbose_name="课程名称")
    course_scores = models.FloatField(verbose_name="学分")
    college = models.ForeignKey(College, on_delete=models.CASCADE, verbose_name="所属学院")
    teacher_name = models.CharField(max_length=20, verbose_name="授课教师")
    semester = models.CharField(max_length=100, choices=(('spring', '春'), ('autumu', '秋')), verbose_name="学期")
    description = models.TextField(verbose_name="课程描述")

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = '课程'

    def __str__(self):
        return str(self.course_name)


class Usercourse(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    scores = models.IntegerField(validators=[MaxValueValidator(100),
                                             MinValueValidator(0)], null=True, verbose_name="分数")

    class Meta:
        verbose_name = '成绩'
        verbose_name_plural = '成绩'

    def __str__(self):
        return str(self.user_name)
