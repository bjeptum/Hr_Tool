from django.contrib import admin
from .models import Department, Employee, FeedbackConfig, Feedback

admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(FeedbackConfig)
admin.site.register(Feedback)
