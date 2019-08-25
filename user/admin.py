from django.contrib import admin
from user.models import vendor

class vendorAdmin(admin.ModelAdmin):
    list_display=['id','Category','Item_desc','Vendor_name','Vendor_loc','Approval','Project','Quality_Comments','Quality_Rating','SCM_Comments','SCM_Rating','PMG_Comments','PMG_Rating','Engineering_Comments','Engineering_Rating','Erection_Comments','Erection_Rating','Commissioning_Comments','Commissioning_Rating','Finance_Comments','Finance_Rating']

admin.site.register(vendor,vendorAdmin)
