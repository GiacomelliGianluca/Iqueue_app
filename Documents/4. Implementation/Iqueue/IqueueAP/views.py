from typing import Any

from django.shortcuts import render, redirect

# Create your views here.

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from Iqueue.forms import RegistrationForm, LogIn
from IqueueAP.models import Account
from Iqueue.forms import ShopForm
from IqueueAP.models import Shop

def success(request):
    return render(request, 'registrationSuccessful.html')


def selectRole(request):
    return render(request, 'SelectRole.html')


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Proccess the data

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            account_id = form.cleaned_data['account_id']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            birthday = form.cleaned_data['birthday']

            account = Account(name=first_name, surname=last_name, account_id=account_id, password=password, email=email, birthday=birthday)

            account.save()

            return redirect('success')
    else:
        form = RegistrationForm()

    return render(request, 'formRegistration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LogIn(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                account = Account.objects.get(email=email, password=password)
                return render(request, 'SelectRole.html')
            except Account.DoesNotExist:
                error = 'Credenziali non valide'
                form.add_error(None, error)
        else:
            error = 'Dati del modulo non validi'
    else:
        form = LogIn()
        error = None

    return render(request, 'login.html', {'form': form, 'error': error})

def account_view(request):
    account = Account.objects.all()
    return render(request, 'account_list.html', {'account': account}) 

def ShopOwner_view(request):
    return render(request, 'ShopOwner.html')

def Shop_view(request):
    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            location = form.cleaned_data['location']
            max_numb_clients = form.cleaned_data['max_numb_clients']
            id_shop = form.cleaned_data['id_shop']
            address = form.cleaned_data['address']
            category = form.cleaned_data['category']
            
            shop = Shop(name=name, location=location, max_numb_clients=max_numb_clients, id_shop=id_shop, address=address, category=category)

            shop.save()
            
            return redirect('SuccessShopRegistration')
    else:
        form = ShopForm()


    return render(request, 'ShopRegistration.html', {'form': form})


def SuccessShopRegistration(request):
    shop = Shop.objects.all()
    return render(request, 'ShopList.html', {'shop': shop})

def Customer_view(request):
    return render(request, 'Customer.html')

def Customer_bakery_view(request):
    
    shop = Shop.objects.filter(category='bakery').values()
    return render(request, 'bakery.html', {'shop': shop})

