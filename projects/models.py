from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import datetime
import uuid
import os
# Create your models here.

CHOICES = (('$', "Dollar"),(u'\u00A3',"Pound"),(u'\u20AC', "Euro"))

class Staff(models.Model):
    #Don't add active user has it covered for you
    user =  models.OneToOneField(User)
    type = models.CharField(max_length = 50)
    phone = models.CharField(max_length=16)
    picture = models.ImageField(upload_to="profile_pictures", blank = False)
    full_name = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=4, decimal_places=2, default= 5)
    
    def update_rating(self):
        whole = self.allocation_set.objects.all()
        total = len(whole);
        completed = len(whole.filter(active=True))
        failed = whole.filter(active=False)
        lost=0
        for fail in failed:
            lost += fail.pay
        #Not complete yet
        self.rating =  (completed/total)*50
        self.save()

    def save(self, *args, **kwargs):
        self.full_name = (self.user.first_name + " " + self.user.last_name)
        super(Staff, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.full_name)

class Project(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    client = models.CharField(max_length = 50)
    client_mail = models.EmailField()
    cost = models.PositiveIntegerField(default=0)
    revenue = models.PositiveIntegerField(default=0)
    pay_type = models.CharField(choices = CHOICES, default = '$', max_length =2)
    start_date = models.DateField()
    last_updated = models.DateTimeField(default=datetime.now)
    estimated_end_date = models.DateField()
    completed = models.BooleanField(default= False)
    completed_date = models.DateField(null = True)
    success = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        #print "Project saved"
        super(Project, self).save(*args, **kwargs)
    
    def update_time(self):
        self.last_updated =datetime.now()
        self.save()
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
                temp = None
            if temp:
                revenue += temp

        self.revenue = revenue
        self.save()
                
class Message(models.Model):
    time = models.DateTimeField(default = datetime.now)
    text = models.CharField(max_length = 500)
    project = models.ForeignKey(Project, null = False)
    to = models.ManyToManyField(User, related_name = "reciever")
    frm = models.ForeignKey(User, related_name = "sender", null = False)

    def __unicode__(self):
        return str(self.text)


class Milestone(models.Model):
    url_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 500)
    cost = models.PositiveIntegerField(default=0)
    start_date = models.DateField()
    deadline = models.DateField()
    project = models.ForeignKey(Project, null = True)
    important = models.BooleanField(default = False)
    completed = models.BooleanField(default= False)
    paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        #print "Milestone saved!"
        Project.objects.get(id = self.project_id).save()
        super(Milestone, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.title)


class Allocation(models.Model):
    milestone = models.ForeignKey(Milestone, null = False)
    person = models.ForeignKey(Staff, null = False)
    pay = models.PositiveIntegerField(null = False)
    pay_type = models.CharField(choices = CHOICES, default ='$', max_length =2)
    active = models.BooleanField(default= False)

    def __unicode__(self):
        return self.pay_type + str(self.pay)

    def save(self, *args, **kwargs):
        self.person.update_rating()
        super(Allocation, self).save(*args, **kwargs)

class Attachment(models.Model):
    file = models.FileField(upload_to='attachments')
    milestone = models.ForeignKey(Milestone, null=True)

    def __unicode__(self):
        return os.path.basename(self.file.name)

class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, null = False)
    date = models.DateField(default = datetime.now)
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField(null = False)
    
    def __unicode__(self):
        return "ID: " + str(self.id)

class Details(models.Model):
    invoice = models.ForeignKey(Invoice, null = False)
    title = models.CharField(max_length = 50)
    desc = models.CharField(max_length = 20)
    cost = models.PositiveIntegerField()
    qty = models.PositiveIntegerField()
    
    def __unicode__(self):
        return "Name: " + self.title + "Cost: " + str(self.cost)
