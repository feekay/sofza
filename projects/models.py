from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import datetime
import uuid
import os
# Create your models here.

CHOICES = (('$', "Dollar"),(u'\u00A3',"Pound"),(u'\u20AC', "Euro"))

class Staff(models.Model):
    user =  models.OneToOneField(User)
    type = models.CharField(max_length = 50)
    phone = models.CharField(max_length=16)
    picture = models.ImageField(upload_to="profile_pictures", blank = False)
    
    def __unicode__(self):
        return str(self.user.username)

class Allocation(model.Model):
    milestone = models.ForeignKey(Milestone, null = False)
    person = models.ForeignKey(Staff, null = False)
    pay = models.IntegerField(null = False)
    pay_type = models.(choices = CHOICES, default ='$', max_length =2)
    active = models.BooleanField(default= False)
    
    def save(self):
        self.pay_type = Project.objects.get(id= self.milestone.project).pay_type
    
    def __unicode__(self):
        return self.pay_type + str(self.pay)

class Project(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    client = models.CharField(max_length = 50)
    client_mail = models.EmailField()
    cost = models.IntegerField(default=0)
    revenue = models.IntegerField(default=0)
    pay_type = models.CharField(choices = CHOICES, default = '$', max_length =2)
    start_date = models.DateField()
    last_updated = models.DateTimeField()
    estimated_end_date = models.DateField()
    completed = models.BooleanField(default= False)
    success = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.last_updated =datetime.now()
        if not self.id:
            self.id = uuid.uuid4()
        #print "Project saved"
        super(Project, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.title + " ID: " + str(id)
    def update_cost(self):
        milestones = self.milestone_set.all()
        self.cost = 0
        for milestone in milestones:
            self.cost += milestone.cost
        self.save()

    def calculate_revenue(self):
        revenue = 0
        milestones = self.milestone_set.all()
        for milestone in milestones:
            try:
                temp= milestone.allocation_set.get(active = True).pay
            except:
                pass
            if temp:
                revenue += temp
    
        self.revenue = revenue
        self.save()
                
class Message(models.Model):
    text = models.CharField(max_length = 500)
    project = models.ForeignKey(Project, null = False)
    to = models.ManyToManyField(User, null = True)
    frm = models.ForeignKey(User, null = False)

    def __unicode__(self):
        return str(self.text)


class Milestone(models.Model):
    url_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 500)
    cost = models.IntegerField(default=0)
    start_date = models.DateField()
    deadline = models.DateField()
    project = models.ForeignKey(Project, null = True)
    completed = models.BooleanField(default= False)
    paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        #print "Milestone saved!"
        super(Milestone, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.title)


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments')
    milestone = models.ForeignKey(Milestone, null=True)

    def __unicode__(self):
        return os.path.basename(self.file.name)


