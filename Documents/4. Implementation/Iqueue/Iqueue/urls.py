"""
URL configuration for Iqueue project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from IqueueAP.views import InitialLoading, scan_qr
from IqueueAP.views import registration_view, login_view
from IqueueAP.views import success
from IqueueAP.views import selectRole
from IqueueAP.views import account_view
from IqueueAP.views import ShopOwner_view
from IqueueAP.views import Shop_view
from IqueueAP.views import Product_view
from IqueueAP.views import SuccessShopRegistration
from IqueueAP.views import Customer_view
from IqueueAP.views import Booking_view
#from IqueueAP.views import Customer_category_view
from IqueueAP.views import Booking_view
from IqueueAP.views import MyShops_view


urlpatterns = [
    path('', InitialLoading, name='InitialLoading'),
    path('login/', login_view, name='login_View'),
    path('registration/', registration_view, name='registration'),
    path('registration/success/', success, name='success'),
    #path('Customer/bakery/qr_code', qr_generation ,name='qr' )
    path('login/SelectRole/', selectRole, name='selectRole'),
    path('account/', account_view, name='account_view'), #Serve??
    path('ShopOwner/', ShopOwner_view, name='ShopOwner_view'),
    path('ShopOwner/Shop/', Shop_view, name='Shop_view'),
    path('ShopOwner/Shop/myshops/', MyShops_view, name='MyShops_view'),
    path('ShopOwner/Product/', Product_view, name='Product_view'),
    path('ShopOwner/Shop/Shoplist/',SuccessShopRegistration, name='SuccessShopRegistration'),
    path('Customer/', Customer_view, name='Customer_view'),
    path('Customer/(?P<selected_category>\s+)/', Booking_view, name='Booking_view'),
    path("admin/", admin.site.urls),
    #path('Customer/bakery/', booking, name='booking'),
    #path('booking-submit', bookingSubmit, name='bookingSubmit'),
    path('ShopOwner/Scan/', scan_qr, name='scan'),

]

#Io farei che dopo la registration, si riparte sempre dal login



