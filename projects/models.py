from django.db import models
from datetime import datetime
import uuid
import os
# Create your models here.

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    client = models.CharField(max_length = 50)
    client_mail = models.EmailField()
    cost = models.IntegerField()
    start_date = models.DateField()
    last_updated = models.DateField()
    estimated_end_date = models.DateField()
    completed = models.BooleanField(default= False)

    def save(self, *args, **kwargs):
        self.last_updated =datetime.now()
        if not self.id:
            self.id = uuid.uuid4()
        print "TEST"
        super(Project, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.title + " ID: " + str(id)

class Milestone(models.Model):
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 500)
    start_date = models.DateField()
    deadline = models.DateField()
    project = models.ForeignKey(Project, null = True)

    def save(self, *args, **kwargs):
        #project = kwargs.pop("project")
        print "HEREEEEE!"
        print self.project_id
        super(Milestone, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.title)

    
class Attachment(models.Model):
    file = models.FileField(upload_to='attachments')
    milestone = models.ForeignKey(Milestone, null=True)

    def __unicode__(self):
        return os.path.basename(self.file.name)