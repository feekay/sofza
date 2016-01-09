from django.contrib import admin
from projects.models import Project, Milestone, Attachment, Staff
# Register your models here.
admin.site.register(Project)
admin.site.register(Staff)
admin.site.register(Milestone)
admin.site.register(Attachment)
