from django.db import models

# Create your models here.

class eMail(models.Model):
    name= models.CharField(max_length =50, null=True)
    email = models.EmailField(unique=True)
    
    
    def save(self, *args, **kwargs):
        super(eMail, self).save(*args, **kwargs)
    
    def __str__(self):
        return (self.email)

    def __unicode__(self):
        return self.name + "  "+ str(self.email)
        
