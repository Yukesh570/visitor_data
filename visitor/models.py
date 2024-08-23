from django.db import models

# Create your models here.
class Visitor_data(models.Model):
    name=models.CharField(max_length=100, null=True,blank=True)
    phone_no= models.IntegerField(null=True , blank=True)
    address=models.CharField(max_length=200, null=True,blank=True)
    email=models.EmailField(max_length=200, null=True,blank=True)
    no_of_person=models.IntegerField(null=True , blank=True)
    purpose=models.CharField(max_length=200,null=True,blank=True)
    image=models.TextField(null=True, blank=True)
    # created_at=models.DateTimeField(null=True, blank=True)