from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from user.forms import userform,vendor1form,vendor2form
from user.models import vendor
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.forms.models import model_to_dict
from graphos.sources.model import *
from graphos.renderers import gchart
from django.contrib.auth.decorators import login_required
def register(request):
    if request.method == 'POST':
        form=userform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your Account has been successfully created')
            return redirect('login')
    else:
        form= userform()
    return render(request,'user/register.html',{'form': form})
@login_required
def home(request):
    return render(request, 'user/home.html')
@login_required
def calcAvg(request,pk):
    x=vendor.objects.get(pk=pk)
    y=vendor.objects.filter(Category=x.Category,Item_desc=x.Item_desc,Vendor_name=x.Vendor_name,Vendor_loc=x.Vendor_loc,Approval=x.Approval)
    count=0
    sum=0
    for i in y:
        if(i.Project_Rating):
            sum+=i.Project_Rating
            count+=1
    if(sum==0):
        for i in y:
            i.Average_Rating=0
            i.save()
    else:
        for i in y:
            i.Average_Rating=sum/count
            i.save()
@login_required
def vendorproadd(request,pk):
    try:
        x=vendor.objects.get(pk=pk)
    except(Exception):
        return redirect('display2')
    if request.method == 'POST':
        form= vendor2form(request.POST)
        form.fields['Project'].required=True
        for i in form.fields:
            form.fields[i].widget.attrs['readonly']=True
            if i=='Approval':
                break
        if form.is_valid():
            q=form.save()
            if(x.Project==None):
                x.delete()
            prorat=0
            count=0
            if(q.Quality_Rating):
                count+=1
            else:
                q.Quality_Rating=0
                q.save()
            if(q.SCM_Rating):
                count+=1
            else:
                q.SCM_Rating=0
                q.save()
            if(q.PMG_Rating):
                count+=1
            else:
                q.PMG_Rating=0
                q.save()
            if(q.Engineering_Rating):
                count+=1
            else:
                q.Engineering_Rating=0
                q.save()
            if(q.Erection_Rating):
                count+=1
            else:
                q.Erection_Rating=0
                q.save()
            if(q.Commissioning_Rating):
                count+=1
            else:
                q.Commissioning_Rating=0
                q.save()
            if(q.Finance_Rating):
                count+=1
            else:
                q.Finance_Rating=0
                q.save()
            if count!=0:
                prorat=(q.Quality_Rating+q.SCM_Rating+q.PMG_Rating+q.Engineering_Rating+q.Erection_Rating+q.Commissioning_Rating+q.Finance_Rating)/count
                q.Project_Rating=prorat
                q.save()
                calcAvg(request,q.pk)
            else:
                prorat=0
                q.Project_Rating=prorat
                q.save()
                calcAvg(request,q.pk)
            messages.success(request,'Vendor Project Has Been Successfully Added')
            return redirect('display2')
    else:
        form= vendor2form(initial=model_to_dict(x,exclude=['Project','Quality_Comments','Quality_Rating','SCM_Comments','SCM_Rating','PMG_Comments','PMG_Rating','Engineering_Comments','Engineering_Rating','Erection_Comments','Erection_Rating','Commissioning_Comments','Commissioning_Rating','Finance_Comments','Finance_Rating']))
        for i in form.fields:
            form.fields[i].widget.attrs['readonly']=True
            if i=='Approval':
                break
    return render(request,'user/vendorform1.html',{'form': form})
@login_required
def vendor1view(request):
    if request.method == 'POST':
        form= vendor1form(request.POST)
        if form.is_valid():
            x=vendor.objects.filter(Category__iexact=request.POST['Category'],Item_desc__iexact=request.POST['Item_desc'],Vendor_name__iexact=request.POST['Vendor_name'],Vendor_loc__iexact=request.POST['Vendor_loc'])
            print(len(list(x)))
            if(len(list(x))!=0):
                messages.warning(request,'Vendor With These Credentials Already Exists!!')
            else:
                request.POST=request.POST.copy()
                request.POST['Category']=request.POST['Category'][0].upper()+request.POST['Category'][1:].lower()
                request.POST['Item_desc']=request.POST['Item_desc'][0].upper()+request.POST['Item_desc'][1:].lower()
                request.POST['Vendor_name']=request.POST['Vendor_name'][0].upper()+request.POST['Vendor_name'][1:].lower()
                request.POST['Vendor_loc']=request.POST['Vendor_loc'][0].upper()+request.POST['Vendor_loc'][1:].lower()
                vendor.objects.get_or_create(Category=request.POST['Category'],Item_desc=request.POST['Item_desc'],Vendor_name=request.POST['Vendor_name'],Vendor_loc=request.POST['Vendor_loc'],Approval=request.POST['Approval'])
                messages.success(request,'Vendor Added Successfully!!')
            return redirect('vendor')
    else:
        form=vendor1form()
    return render(request,'user/vendorform1.html',{'form': form})
@login_required
def vendor1Update(request,pk):
    try:
        x=vendor.objects.get(pk=pk)
    except(Exception):
        return redirect('display2')
    if request.method=='POST':
        request.POST=request.POST.copy()
        if(request.POST['Quality_Rating']==""):
            request.POST['Quality_Rating']=0
        if(request.POST['SCM_Rating']==""):
            request.POST['SCM_Rating']=0
        if(request.POST['PMG_Rating']==""):
            request.POST['PMG_Rating']=0
        if(request.POST['Engineering_Rating']==""):
            request.POST['Engineering_Rating']=0
        if(request.POST['Erection_Rating']==""):
            request.POST['Erection_Rating']=0
        if(request.POST['Commissioning_Rating']==""):
            request.POST['Commissioning_Rating']=0
        if(request.POST['Finance_Rating']==""):
            request.POST['Finance_Rating']=0
        if(int(request.POST['Quality_Rating'])>100 or int(request.POST['SCM_Rating'])>100 or int(request.POST['PMG_Rating'])>100 or int(request.POST['Engineering_Rating'])>100 or int(request.POST['Erection_Rating'])>100 or int(request.POST['Commissioning_Rating'])>100 or int(request.POST['Finance_Rating'])>100):
            messages.warning(request,'Rating Can Only Be Less Than 100')
            return redirect("vendor-update",pk=pk)
        x.Quality_Comments=request.POST['Quality_Comments'] or None
        x.SCM_Comments=request.POST['SCM_Comments'] or None
        x.PMG_Comments=request.POST['PMG_Comments'] or None
        x.Engineering_Comments=request.POST['Engineering_Comments'] or None
        x.Erection_Comments=request.POST['Erection_Comments'] or None
        x.Commissioning_Comments=request.POST['Commissioning_Comments'] or None
        x.Finance_Comments=request.POST['Finance_Comments'] or None
        x.Quality_Rating=int(request.POST['Quality_Rating']) if request.POST['Quality_Rating'] else None
        x.SCM_Rating=int(request.POST['SCM_Rating']) if request.POST['SCM_Rating'] else None
        x.PMG_Rating=int(request.POST['PMG_Rating']) if request.POST['PMG_Rating'] else None
        x.Engineering_Rating=int(request.POST['Engineering_Rating']) if request.POST['Engineering_Rating'] else None
        x.Erection_Rating=int(request.POST['Erection_Rating']) if request.POST['Erection_Rating'] else None
        x.Commissioning_Rating=int(request.POST['Commissioning_Rating']) if request.POST['Commissioning_Rating'] else None
        x.Finance_Rating=int(request.POST['Finance_Rating']) if request.POST['Finance_Rating'] else None
        x.save()
        prorat=0
        count=0
        if(x.Quality_Rating):
            count+=1
        else:
            x.Quality_Rating=0
        if(x.SCM_Rating):
            count+=1
        else:
            x.SCM_Rating=0
        if(x.PMG_Rating):
            count+=1
        else:
            x.PMG_Rating=0
        if(x.Engineering_Rating):
            count+=1
        else:
            x.Engineering_Rating=0
        if(x.Erection_Rating):
            count+=1
        else:
            x.Erection_Rating=0
        if(x.Commissioning_Rating):
            count+=1
        else:
            x.Commissioning_Rating=0
        if(x.Finance_Rating):
            count+=1
        else:
            x.Finance_Rating=0
        if count!=0:
            prorat=(x.Quality_Rating+x.SCM_Rating+x.PMG_Rating+x.Engineering_Rating+x.Erection_Rating+x.Commissioning_Rating+x.Finance_Rating)/count
            x.Project_Rating=prorat
            x.save()
            messages.success(request,'Updated Successfully!!')
            calcAvg(request,x.pk)
        return redirect("display2")
    else:
        form= vendor2form(initial=model_to_dict(x))
        for i in form.fields:
            form.fields[i].widget.attrs['readonly']=True
            if i=='Project':
                break
        return render(request,'user/vendorupdateform.html',{'form': form})


@login_required
def display(request):
    a=vendor.objects.all()
    return render(request,"user/display.html",{'a':a})
@login_required
def display2(request):
    a=vendor.objects.all().order_by('Category','Project')
    return render(request,"user/display2.html",{'a':a})
@login_required
def filter(request):
    vname=request.POST['Vendor_name']
    idesc=request.POST['Item_desc']
    loc=request.POST['Vendor_loc']
    rat=int(request.POST['Overall'])
    cat=request.POST['Category']
    a=queryfilter(request,vname,idesc,loc,rat,cat)
    if(len(list(a))==0):
        messages.warning(request,'No Record Exists')
    return render(request,"user/display.html",{'a':a})
@login_required
def filter2(request):
    vname=request.POST['Vendor_name']
    idesc=request.POST['Item_desc']
    loc=request.POST['Vendor_loc']
    rat=int(request.POST['Overall'])
    cat=request.POST['Category']
    a=queryfilter(request,vname,idesc,loc,rat,cat)
    if(len(list(a))==0):
        messages.warning(request,'No Record Exists')
    return render(request,"user/display2.html",{'a':a})

@login_required
def deletepro(request,pk):
    try:
        x=vendor.objects.get(pk=pk)
    except(Exception):
        return redirect('display2')
    temp=x
    x.delete()
    y=vendor.objects.filter(Category=temp.Category,Item_desc=temp.Item_desc,Vendor_name=temp.Vendor_name,Vendor_loc=temp.Vendor_loc,Approval=temp.Approval)
    count=0
    sum=0
    for i in y:
        if(i.Project_Rating):
            sum+=i.Project_Rating
            count+=1
    if(sum==0):
        for i in y:
            i.Average_Rating=0
            i.save()
    else:
        for i in y:
            i.Average_Rating=sum/count
            i.save()
    return redirect('display2')
@login_required
def queryfilter(request,vname,idesc,loc,rat,cat):
    if(vname=='None' and idesc=='None' and loc=='None' and rat==0 and cat=='None'):
        return vendor.objects.all()
    elif(vname=='None' and idesc=='None' and loc=='None' and rat==0 and cat!='None'):
        return vendor.objects.filter(Category__iexact=cat)
    elif(vname=='None' and idesc=='None' and loc=='None' and rat!=0 and cat=='None'):
        return vendor.objects.filter(Average_Rating__gte=rat)
    elif(vname=='None' and idesc=='None' and loc=='None' and rat!=0 and cat!='None'):
        return vendor.objects.filter(Average_Rating__gte=rat,Category__iexact=cat)
    elif(vname=='None' and idesc=='None' and loc!='None' and rat==0 and cat=='None'):
        return vendor.objects.filter(Vendor_loc__iexact=loc)
    elif(vname=='None' and idesc=='None' and loc!='None' and rat==0 and cat!='None'):
        return vendor.objects.filter(Vendor_loc__iexact=loc,Category__iexact=cat)
    elif(vname=='None' and idesc=='None' and loc!='None' and rat!=0 and cat=='None'):
        return vendor.objects.filter(Vendor_loc__iexact=loc,Average_Rating__gte=rat)
    elif(vname=='None' and idesc=='None' and loc!='None' and rat!=0 and cat!='None'):
        return vendor.objects.filter(Vendor_loc__iexact=loc,Average_Rating__gte=rat,Category__iexact=cat)
    elif(vname=='None' and idesc!='None' and loc=='None' and rat==0 and cat=='None'):
        return vendor.objects.filter(Item_desc__iexact=idesc)
    elif(vname=='None' and idesc!='None' and loc=='None' and rat==0 and cat!='None'):
        return vendor.objects.filter(Item_desc__iexact=idesc,Category__iexact=cat)
    elif(vname=='None' and idesc!='None' and loc=='None' and rat!=0 and cat=='None'):
        return vendor.objects.filter(Item_desc__iexact=idesc,Average_Rating__gte=rat)
    elif(vname=='None' and idesc!='None' and loc=='None' and rat!=0 and cat!='None'):
        return vendor.objects.filter(Item_desc__iexact=idesc,Average_Rating__gte=rat,Category__iexact=cat)
    elif(vname=='None' and idesc!='None' and loc!='None' and rat==0 and cat=='None'):
        return vendor.objects.filter(Item_desc__iexact=idesc,Vendor_loc__iexact=loc)
    elif(vname=='None' and idesc!='None' and loc!='None' and rat==0 and cat!='None'):
        return vendor.objects.filter(Item_desc__iexact=idesc,Vendor_loc__iexact=loc,Category__iexact=cat)
    elif(vname=='None' and idesc!='None' and loc!='None' and rat!=0 and cat=='None'):
        return vendor.objects.filter(Item_desc__iexact=idesc,Vendor_loc__iexact=loc,Average_Rating__gte=rat)
    elif(vname=='None' and idesc!='None' and loc!='None' and rat!=0 and cat!='None'):
        return vendor.objects.filter(Item_desc__iexact=idesc,Vendor_loc__iexact=loc,Average_Rating__gte=rat,Category__iexact=cat)
    elif(vname!='None' and idesc=='None' and loc=='None' and rat==0 and cat=='None'):
        return vendor.objects.filter(Vendor_name__iexact=vname)
    elif(vname!='None' and idesc=='None' and loc=='None' and rat==0 and cat!='None'):
        return vendor.objects.filter(Vendor_name__iexact=vname,Category__iexact=cat)
    elif(vname!='None' and idesc=='None' and loc=='None' and rat!=0 and cat=='None'):
        return vendor.objects.filter(Vendor_name__iexact=vname,Average_Rating__gte=rat)
    elif(vname!='None' and idesc=='None' and loc=='None' and rat!=0 and cat!='None'):
        return vendor.objects.filter(Vendor_name__iexact=vname,Average_Rating__gte=rat,Category__iexact=cat)
    elif(vname!='None' and idesc=='None' and loc!='None' and rat==0 and cat=='None'):
        return vendor.objects.filter(Vendor_name__iexact=vname,Vendor_loc__iexact=loc)
    elif(vname!='None' and idesc=='None' and loc!='None' and rat==0 and cat!='None'):
        return vendor.objects.filter(Vendor_name__iexact=vname,Vendor_loc__iexact=loc,Category__iexact=cat)
    elif(vname!='None' and idesc=='None' and loc!='None' and rat!=0 and cat=='None'):
        return vendor.objects.filter(Vendor_name__iexact=vname,Vendor_loc__iexact=loc,Average_Rating__gte=rat)
    elif(vname!='None' and idesc=='None' and loc!='None' and rat!=0 and cat!='None'):
        return vendor.objects.filter(Vendor_name__iexact=vname,Vendor_loc__iexact=loc,Average_Rating__gte=rat,Category__iexact=cat)
    elif(vname!='None' and idesc!='None' and loc=='None' and rat==0 and cat=='None'):
        return vendor.objects.filter(Vendor_name__iexact=vname,Item_desc__iexact=idesc)
    elif(vname!='None' and idesc!='None' and loc=='None' and rat==0 and cat!='None'):
        return vendor.objects.filter(Vendor_name__iexact=vname,Item_desc__iexact=idesc,Category__iexact=cat)
    elif(vname!='None' and idesc!='None' and loc=='None' and rat!=0 and cat=='None'):
        return vendor.objects.filter(Vendor_name__iexact=vname,Item_desc__iexact=idesc,Average_Rating__gte=rat)
    elif(vname!='None' and idesc!='None' and loc=='None' and rat!=0 and cat!='None'):
        return vendor.objects.filter(Vendor_name__iexact=vname,Item_desc__iexact=idesc,Average_Rating__gte=rat,Category__iexact=cat)
    elif(vname!='None' and idesc!='None' and loc!='None' and rat==0 and cat=='None'):
        return vendor.objects.filter(Vendor_name__iexact=vname,Item_desc__iexact=idesc,Vendor_loc__iexact=loc)
    elif(vname!='None' and idesc!='None' and loc!='None' and rat==0 and cat!='None'):
        return vendor.objects.filter(Vendor_name__iexact=vname,Item_desc__iexact=idesc,Vendor_loc__iexact=loc,Category__iexact=cat)
    elif(vname!='None' and idesc!='None' and loc!='None' and rat!=0 and cat=='None'):
        return vendor.objects.filter(Vendor_name__iexact=vname,Item_desc__iexact=idesc,Vendor_loc__iexact=loc,Average_Rating__gte=rat)
    elif(vname!='None' and idesc!='None' and loc!='None' and rat!=0 and cat!='None'):
        return vendor.objects.filter(Vendor_name__iexact=vname,Item_desc__iexact=idesc,Vendor_loc__iexact=loc,Average_Rating__gte=rat,Category__iexact=cat)

@login_required
def grphosxx(request):
    maxpro=[]
    if request.method=='POST':
        vname=request.POST['Vendor_name']
        idesc=request.POST['Item_desc']
        loc=request.POST['Vendor_loc']
        rat=int(request.POST['Overall'])
        cat=request.POST['Category']
        queryset=queryfilter(request,vname,idesc,loc,rat,cat)
        print(queryset)
    else:
        queryset = vendor.objects.all()
    data=[['Vendor Name']]
    for i in queryset:
        maxpro.append(i.Project)
    maxpro=list(set(maxpro))
    if None in maxpro:
        maxpro.remove(None)
    if (len(maxpro)==0):
        messages.warning(request,'Vendor Not Found!!')
        return redirect("display2")
    for i in range(1,max(set(maxpro))+1):
        data[0].append('Project'+' '+str(i)+' Rating')
    vendors=queryset.values('Category','Item_desc','Vendor_name','Vendor_loc','Approval').distinct()
    for i in vendors:
        inlist=[]
        veninf=vendor.objects.filter(Category=i['Category'],Item_desc=i['Item_desc'],Vendor_name=i['Vendor_name'],Vendor_loc=i['Vendor_loc'],Approval=i['Approval'])
        inlist.append(veninf[0].Category+'|'+veninf[0].Vendor_name+'|'+veninf[0].Vendor_loc)
        for j in range(1,max(set(maxpro))+1):
            l=veninf.filter(Project=j)
            if len(l)==0:
                inlist.append(0)
            else:
                inlist.append(l[0].Project_Rating)
        data.append(inlist)
    data_source1 = SimpleDataSource(data)
    chart1 = gchart.ColumnChart(data_source1,options={'title':'Rating of different Vendors'},width='100%',height=800)
    return render(request,'graph.html',{'chart1':chart1})
@login_required
def grphosxxx(request):
    if request.method=='POST':
        vname=request.POST['Vendor_name']
        idesc=request.POST['Item_desc']
        loc=request.POST['Vendor_loc']
        rat=int(request.POST['Overall'])
        cat=request.POST['Category']
        queryset=queryfilter(request,vname,idesc,loc,rat,cat)
        vendors=queryset.values('Category','Item_desc','Vendor_name','Vendor_loc','Approval').distinct()
    else:
        vendors=vendor.objects.values('Category','Item_desc','Vendor_name','Vendor_loc','Approval').distinct()
    if(len(list(vendors))==0):
        messages.warning(request,'No Data Found!!')
        return redirect("display2")
    data=[['Vendor Name','Overall Rating']]
    for i in vendors:
        veninf=vendor.objects.filter(Category=i['Category'],Item_desc=i['Item_desc'],Vendor_name=i['Vendor_name'],Vendor_loc=i['Vendor_loc'],Approval=i['Approval'])
        new=[]
        new.append(veninf[0].Vendor_name+'|'+veninf[0].Category+'|'+veninf[0].Vendor_loc)
        new.append(veninf[0].Average_Rating)
        data.append(new)
    data_source1 = SimpleDataSource(data)
    chart1 = gchart.ColumnChart(data_source1,options={'title':'Overall Rating of different Vendors'},width='100%',height=800)
    return render(request,'graph2.html',{'chart1':chart1})
@login_required
def vendor_del(request,pk):
    try:
        temp=vendor.objects.get(pk=pk)
    except(Exception):
        return redirect('display2')
    b=vendor.objects.filter(Category=temp.Category,Item_desc=temp.Item_desc,Vendor_name=temp.Vendor_name,Vendor_loc=temp.Vendor_loc,Approval=temp.Approval)
    if len(list(b))==0:
        messages.warning(request,'Something Went Wrong.Please Refresh The Page.')
    for i in b:
        i.delete()
        messages.success(request,'Vendor Deleted Successfully!!')
    return redirect('display2')
