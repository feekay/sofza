from django.contrib import admin
from projects.models import Project, Milestone, Attachment
# Register your models here.
admin.site.register(Project)
admin.site.register(Milestone)
admin.site.register(Attachment)
