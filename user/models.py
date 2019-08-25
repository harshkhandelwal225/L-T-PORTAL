from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
class vendor(models.Model):
    q1=[('Approved','Approved'),('Documents Required','Documents Required')]
    class Meta:
        unique_together=(('Category','Item_desc','Vendor_name','Vendor_loc','Approval','Project'))
    Category = models.CharField(max_length=50)
    Item_desc = models.CharField(max_length=200)
    Vendor_name = models.CharField(max_length=100)
    Vendor_loc = models.CharField(max_length=120)
    Approval = models.CharField(max_length=50)
    Average_Rating = models.IntegerField(blank=True, null=True)
    Project = models.PositiveIntegerField(validators=[MaxValueValidator(100),MinValueValidator(1)],blank=True, null=True)
    Project_Rating = models.IntegerField(blank=True, null=True)
    Quality_Comments = models.CharField(max_length=500,blank=True, null=True)
    Quality_Rating = models.PositiveIntegerField(validators=[MaxValueValidator(100),],blank=True,null=True)
    SCM_Comments= models.CharField(max_length=500,blank=True, null=True)
    SCM_Rating = models.PositiveIntegerField(validators=[MaxValueValidator(100),],blank=True,null=True)
    PMG_Comments= models.CharField(max_length=500,blank=True, null=True)
    PMG_Rating= models.PositiveIntegerField(validators=[MaxValueValidator(100),],blank=True,null=True)
    Engineering_Comments = models.CharField(max_length=500,blank=True, null=True)
    Engineering_Rating= models.PositiveIntegerField(validators=[MaxValueValidator(100),],blank=True,null=True)
    Erection_Comments = models.CharField(max_length=500,blank=True, null=True)
    Erection_Rating= models.PositiveIntegerField(validators=[MaxValueValidator(100),],blank=True,null=True)
    Commissioning_Comments = models.CharField(max_length=500,blank=True, null=True)
    Commissioning_Rating= models.PositiveIntegerField(validators=[MaxValueValidator(100),],blank=True,null=True)
    Finance_Comments = models.CharField(max_length=500,blank=True, null=True)
    Finance_Rating= models.PositiveIntegerField(validators=[MaxValueValidator(100),],blank=True,null=True)
