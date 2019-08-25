"""projectV URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from user import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',user_views.register,name='register'),
    path('',auth_views.LoginView.as_view(template_name='user/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='user/logout.html'),name='logout'),
    path('home/',user_views.home,name='home'),
    path(r'vendor/<int:pk>',user_views.vendor1Update,name="vendor-update"),
    path(r'delete/<int:pk>',user_views.deletepro,name="vendor-prodelete"),
    path('vendor/',user_views.vendor1view,name="vendor"),
    path('vendoradd/<int:pk>',user_views.vendorproadd,name="vendor-proadd"),
    path('display/',user_views.display,name="display"),
    path('display2/',user_views.display2,name="display2"),
    path('filter/',user_views.filter,name="filter"),
    path('filter2/',user_views.filter2,name="filter2"),
    path('graph/',user_views.grphosxx,name='graph1'),
    path('graph2/',user_views.grphosxxx,name='graph2'),
    path('vendor_del/<int:pk>',user_views.vendor_del,name='vendor_del'),
    ]
