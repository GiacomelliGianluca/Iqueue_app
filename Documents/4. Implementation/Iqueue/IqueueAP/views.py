from datetime import timedelta, datetime

from django.http import JsonResponse

from Iqueue import forms
from io import BytesIO
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
import uuid
import qrcode
import base64
from Iqueue.forms import RegistrationForm, LogIn, ShopForm, Shop_and_day_selectionForm, TimeSlot_selectionForm
from IqueueAP.models import Account, Shop, Product, TimeSlot, Booking
from django.contrib import messages
from qrcode import QRCode
import json

from django.views.decorators.csrf import csrf_exempt


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

            idso = str(uuid.uuid4())
            idc = str(uuid.uuid4())

            account = Account(name=first_name, surname=last_name, password=password, email=email, birthday=birthday,
                              idso=idso, idc=idc)

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
                request.session['idso'] = str(account.idso)
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
            # ids = form.cleaned_data['ids']
            address = form.cleaned_data['address']
            category = form.cleaned_data['category']
            opening_time = form.cleaned_data['opening_time']
            closing_time = form.cleaned_data['closing_time']
            slot_duration = form.cleaned_data['slot_duration']

            idso = request.session.get('idso', '')

            ids = str(uuid.uuid4())

            shop = Shop(name=name, lat=lat, lon=lon, max_numb_clients=max_numb_clients, ids=ids, idso=idso,
                        address=address,
                        rating=0, numb_of_ratings=0, category=category)

            shop.save()

            slot_duration = timedelta(minutes=slot_duration)

            current_date = datetime.now().date()

            end_date = current_date + timedelta(weeks=52)  # time slots definiti per un anno

            time_slots = []

            # SE ABBIAMO tempo creare per giorni diversi ls possibilità di inserire time slots diversi
            while current_date <= end_date:
                if current_date.weekday() < 5:
                    current_datetime = datetime.combine(current_date,
                                                        opening_time)  # current_date: data anno mese giorno; opening_time: ore minuti

                    while current_datetime.time() < closing_time:
                        start_time = current_datetime.time()  # datetime.time individua
                        end_time = (current_datetime + slot_duration).time()
                        if end_time > closing_time:
                            end_time = closing_time

                        date = (current_datetime + slot_duration).date()

                        time_slot = TimeSlot(start=start_time, end=end_time, date=date, available=True, shop=shop)
                        time_slots.append(time_slot)

                        current_datetime += slot_duration

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


# def Booking_view(request):
#     if request.method == 'POST':
#         shop_name = request.POST.get('shop')
#         date = request.POST.get('date')
#         shop = Shop.objects.get(name=shop_name)
#         timeslot = request.POST.get('timeslot')
#         slots = TimeSlot.objects.filter(shop=shop, date=date, available=True)
#         return render(request, 'bakery.html', {'shops': Shop.objects.filter(category='bakery').values(), 'slots': slots})
#     else:
#         return render(request, 'bakery.html', {'shops': Shop.objects.all()})


def Booking_view(request):
    Shop_and_day_form = forms.Shop_and_day_selectionForm()
    TimeSlot_form = forms.TimeSlot_selectionForm()
    if request.method == 'POST':
        if 'btnform1' in request.POST:
            shop_name = request.POST.get('shop')
            date = request.POST.get('date')
            shop = Shop.objects.get(name=shop_name)
            slots = TimeSlot.objects.filter(shop=shop, date=date, available=True)
            addresses = [shop.address for shop in Shop.objects.all()]
            return render(request, 'bakery.html',
                          {'shops': Shop.objects.filter(category='bakery').values(), 'slots': slots,
                           'Shop_and_day_form': Shop_and_day_form, 'TimeSlot_form': TimeSlot_form,
                           'addresses': addresses})

        if 'btnform2' in request.POST and 'selected_slot' in request.POST:
            timeslot_id = request.POST.get('selected_slot')
            timeslot = get_object_or_404(TimeSlot, pk=timeslot_id)
            shop = timeslot.shop
            shop.queue += 1
            shop.save()

            timeslot.available = False
            timeslot.save()

            qr_data = f"Negozio: {shop.name}\nData: {timeslot.date}\nOrario: {timeslot.start} - {timeslot.end}"

            qr_code_img = qrcode.QRCode()
            qr_code_img.add_data(qr_data)
            qr_code_img.make(fit=True)

            image = qr_code_img.make_image(fill="black", back_color="white")
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            buffer.seek(0)
            qr_code_img_str = base64.b64encode(buffer.read()).decode('utf-8')
            addresses = [shop.address for shop in Shop.objects.all()]

            return render(request, 'qr.html', {'qr_code_img': qr_code_img_str, 'time_slot': timeslot_id, 'addresses': addresses})

    addresses = [shop.address for shop in Shop.objects.all()]

    context = {
        'shops': Shop.objects.all(),
        'Shop_and_day_form': Shop_and_day_form,
        'TimeSlot_form': TimeSlot_form,
        'addresses': addresses,
    }

    return render(request, 'bakery.html', context=context)


# def booking(request):
# if request.method == 'POST':
#   shop_name = request.POST.get('shop_name')
#  date = request.POST.get('date')
# Store shop name and date in django session:
# request.session['shop_name'] = shop_name
# request.session['date'] = date

# return redirect('bookingSubmit')

# return render(request, 'booking.html', {'shops': Shop.objects.filter(category='bakery').values()})


# def bookingSubmit(request):
# Get stored data from django session:
# shop_name = request.session.get('shop_name')
# date = request.session.get('date')
# times = [
# "3 PM", "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM", "6:30 PM", "7 PM", "7:30 PM"
# ]
# if request.method == 'POST':
# time = request.POST.get("time")
# BookingForm = Booking.objects.get_or_create(
#                       name = shop_name,
#                      date = date,
#                     time = time,
#                )
# messages.success(request, "Booking Saved!")
# return render(request, 'bookingSubmit.html', {'times': times})


# Da implementare
def Customer_category_view(request):
    shop = Shop.objects.filter(category='bakery').values()
    return render(request, 'category_selection.html', {'shop': shop})


def scan_qr(request):
    if request.method == 'POST':
        qr_code_value = request.POST.get('qrCodeValue')

        qr_code_lines = qr_code_value.split('\n')
        shop_name = qr_code_lines[0].split(': ')[1]
        shop_name = shop_name.strip()
        date_str = qr_code_lines[1].split(': ')[1]
        date_str = date_str.strip()
        time_range_str = qr_code_lines[2].split(': ')[1]
        time_range_str = time_range_str.strip()

        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        start_time_str, end_time_str = time_range_str.split(' - ')
        start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
        end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()

        start_datetime = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)

        try:
            shop = Shop.objects.get(name=shop_name)
        except Shop.DoesNotExist:
            return render(request, 'error.html')

        try:
            time_slot = TimeSlot.objects.get(shop=shop, start=start_datetime, end=end_datetime, date=date)
            if not time_slot.available:
                shop.queue -= 1
                shop.save()
                return render(request, "scan_successful.html")
        except TimeSlot.DoesNotExist:
            return render(request, 'error.html')

    return render(request, 'scan.html')
