from django.db import models
from django.template.defaultfilters import slugify
from datetime import datetime
import uuid
import os
# Create your models here.

class Project(models.Model):
    CHOICES = (('$', "Dollar"),('#',"Pound"),('?', "Euro"))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    client = models.CharField(max_length = 50)
    client_mail = models.EmailField()
    cost = models.IntegerField(default=0)
    #pay_type = models.CharField(choices = CHOICES, default = '$', max_length =2)
    start_date = models.DateField()
    last_updated = models.DateTimeField()
    estimated_end_date = models.DateField()
    completed = models.BooleanField(default= False)

    def save(self, *args, **kwargs):
        self.last_updated =datetime.now()
        if not self.id:
            self.id = uuid.uuid4()
        print "Project saved"
        super(Project, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.title + " ID: " + str(id)

class Milestone(models.Model):
    CHOICES = (('$', "Dollar"),('#',"Pound"),('?', "Euro"))
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 500)
    cost = models.IntegerField(default=0)
    slug = models.SlugField(max_length =50)
    #Delete Pay Type in future and add in project instead
    pay_type = models.CharField(choices = CHOICES, default = '$', max_length =2)
    start_date = models.DateField()
    deadline = models.DateField()
    project = models.ForeignKey(Project, null = True)
    completed = models.BooleanField(default= False)
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        parent = Project.objects.get(id= self.project_id)
        parent.cost += self.cost
        parent.save()
        print "Milestone saved!"
        super(Milestone, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.title)


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments')
    milestone = models.ForeignKey(Milestone, null=True)

    def __unicode__(self):
        return os.path.basename(self.file.name)
