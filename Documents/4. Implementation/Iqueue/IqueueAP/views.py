from datetime import timedelta, datetime

from django.shortcuts import render, redirect

# Create your views here.

from django.views.decorators.csrf import csrf_exempt

from Iqueue.forms import RegistrationForm, LogIn, ShopForm, BookingForm
from IqueueAP.models import Account, Shop, Product, TimeSlot, Booking


def InitialLoading(request):
    return render(request, 'LoadingIqueue.html')


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
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            birthday = form.cleaned_data['birthday']

            account = Account(name=first_name, surname=last_name, password=password, email=email, birthday=birthday)

            account.save()

            return redirect('success')
    else:
        form = RegistrationForm()

    return render(request, 'formRegistration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        # if 'LogIn' in request.POST:
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
            error = 'Inserted data are not valid'
    else:
        form = LogIn()
        error = None
        # if 'RegistrationForm_fromLogIN' in request.POST:
        #    return redirect('registration_view') 

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
            lat = form.cleaned_data['lat']
            lon = form.cleaned_data['lon']
            max_numb_clients = form.cleaned_data['max_numb_clients']
            ids = form.cleaned_data['ids']
            address = form.cleaned_data['address']
            category = form.cleaned_data['category']
            opening_time = form.cleaned_data['opening_time']
            closing_time = form.cleaned_data['closing_time']
            slot_duration = form.cleaned_data['slot_duration']

            shop = Shop(name=name, lat=lat, lon=lon, max_numb_clients=max_numb_clients, ids=ids, address=address,
                        rating=0, numb_of_ratings=0, category=category)

            shop.save()

            slot_duration = timedelta(minutes=slot_duration)

            current_date = datetime.now().date()

            end_date = current_date + timedelta(weeks=2)

            time_slots = []

            current_date = current_date

            while current_date <= end_date:
                if current_date.weekday() < 5:
                    current_datetime = datetime.combine(current_date, opening_time)

                    while current_datetime.time() < closing_time:
                        start_time = current_datetime.time()
                        end_time = (current_datetime + slot_duration).time()
                        date = (current_datetime + slot_duration).date()

                        time_slot = TimeSlot(start=start_time, end=end_time,date=date ,available=True, shop=shop)
                        time_slots.append(time_slot)

                        current_datetime += timedelta(minutes=30)

                current_date += timedelta(days=1)

            TimeSlot.objects.bulk_create(time_slots)

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
    if request.method == 'POST':
        shop_name = request.POST.get('shop')
        date = request.POST.get('date')
        shop = Shop.objects.get(name=shop_name)
        slots = TimeSlot.objects.filter(shop=shop, date=date, available=True)
        selected_slot = request.POST.get('selected_slot')
        booking = Booking.objects.filter(name=shop_name, date=date, time_slot=selected_slot)
        return render(request, 'bakery.html', {'shops': Shop.objects.all(), 'slots': slots, 'booking':booking})
    else:
        return render(request, 'bakery.html', {'shops': Shop.objects.all()})

def Customer_category_view(request):
    shop = Shop.objects.filter(category='bakery').values()
    return render(request, 'category_selection.html', {'shop': shop})
