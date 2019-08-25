from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from user.models import vendor
class userform(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','password1','password2']
class vendor1form(forms.ModelForm):
    q1=(('Approved','Approved'),('Documents Required','Documents Required'))
    Approval=forms.ChoiceField(choices=q1,initial='Documents Required')
    class Meta:
        model = vendor
        fields=['Category','Item_desc','Vendor_name','Vendor_loc','Approval']
        ##exclude = ('Comm_dept1','Comm_dept2','Comm_dept3','Comm_dept4','Project','Average_Rating','Project_Rating')
class vendor2form(forms.ModelForm):
    q1=(('Approved','Approved'),('Documents Required','Documents Required'))
    Approval=forms.ChoiceField(choices=q1)
    class Meta:
        model = vendor
        fields=['Category','Item_desc','Vendor_name','Vendor_loc','Approval','Project','Quality_Comments','Quality_Rating','SCM_Comments','SCM_Rating','PMG_Comments','PMG_Rating','Engineering_Comments','Engineering_Rating','Erection_Comments','Erection_Rating','Commissioning_Comments','Commissioning_Rating','Finance_Comments','Finance_Rating']
