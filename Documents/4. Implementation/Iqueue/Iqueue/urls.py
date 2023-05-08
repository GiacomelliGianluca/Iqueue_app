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
from IqueueAP.views import registration_view, login_view
from IqueueAP.views import success
from IqueueAP.views import selectRole
from IqueueAP.views import account_view
from IqueueAP.views import ShopOwner_view
from IqueueAP.views import Shop_view
from IqueueAP.views import SuccessShopRegistration
urlpatterns = [
    path("admin/", admin.site.urls),
    path('registration/', registration_view, name='registration'),
    path('registration/success/', success, name='success'),
    path('registration/SelectRole/', selectRole, name='selectRole'),
    path('login/', login_view, name='login_View'),
    path('account/', account_view, name='account_view'),
    path('login/ShopOwner/', ShopOwner_view, name='ShopOwner_view'),
    path('registration/SelectRole/ShopOwner/', ShopOwner_view, name='ShopOwner_view'),
    path('registration/SelectRole/ShopOwner/Shop', Shop_view, name='Shop_view'),
    path('login/ShopOwner/Shop/', Shop_view, name='Shop_view'),
    path('login/ShopOwner/Shop/Shoplist/',SuccessShopRegistration, name='SuccessShopRegistration'),
    path('registration/SelectRole/ShopOwner/Shop/Shoplist',SuccessShopRegistration, name='SuccessShopRegistration')
]




