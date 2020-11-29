from django.contrib import admin
from .models import Course, User, Usercourse, College


admin.site.register(Course)
admin.site.register(Usercourse)
admin.site.register(User)
admin.site.register(College)
