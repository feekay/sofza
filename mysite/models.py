from django.db import models
from datetime import datetime
# Create your models here.

class eMail(models.Model):
    name= models.CharField(max_length =50, null=True)
    email = models.EmailField(unique=True)
    details = models.CharField(max_length = 150)
    time = models.DateTimeField(default=datetime.now)    
    
    def save(self, *args, **kwargs):
        super(eMail, self).save(*args, **kwargs)

    def __unicode__(self):
        return  str(self.email)

