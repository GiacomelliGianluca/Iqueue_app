from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
import random

from django.http import JsonResponse
from django.core.exceptions import ValidationError
from Iqueue import forms
from io import BytesIO
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
import uuid
import qrcode
import base64
from Iqueue.forms import RegistrationForm, LogIn, ShopForm, ProductForm, Shop_and_day_selectionForm, \
    TimeSlot_selectionForm, AdvertisementForm
from IqueueAP.models import Account, Shop, Product, TimeSlot, Slot, QR, Review, Advertisement, PurchaseList, \
    PurchasedItem, WishListItem, WishList
from django.db.models import Q
from django.contrib import messages
from qrcode import QRCode
import json
from django.http import HttpResponseRedirect
from django.template import RequestContext

from django.views.decorators.csrf import csrf_exempt


def InitialLoading(request):
    return render(request, 'LoadingIqueue.html')


def success(request):
    return render(request, 'registrationSuccessful.html')


def selectRole(request):
    name = request.session.get('name', '')
    idc = request.session.get('idc', '')
    idso = request.session.get('idso', '')

    #Advertisement
    idss=[]
    for adv in Advertisement.objects.all():
        idss.append(adv.ids)
        #Delating of due advertisements
        if datetime.now().date()== adv.date_end:
            adv.delete()

    shop_advertised = None
    if idss:
        random_ids = random.choice(idss)
        shop_advertised=Shop.objects.filter(ids=random_ids).first()

    return render(request, 'SelectRole.html', {'name': name, 'idc': idc, 'idso': idso, 'shop':shop_advertised})


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

            if birthday > date.today():
                return render(request, 'ErrorBirthdayAccount.html')
                
            if Account.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, 'ErrorEmailAccount.html')
              

            idso = str(uuid.uuid4())
            idc = str(uuid.uuid4())

            account = Account(name=first_name, surname=last_name, password=password, email=email, birthday=birthday,
                              idso=idso, idc=idc)

            account.save()

            purchase_list = PurchaseList(idc=account)

            purchase_list.save()

            wish_list = WishList(idc=account)
            wish_list.save()

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
                request.session['name'] = str(account.name)
                request.session['idc'] = str(account.idc)
                request.session['idso'] = str(account.idso)
                    #Advertisement
                idss=[]
                for adv in Advertisement.objects.all():
                    idss.append(adv.ids)
                    #Delating of due advertisements
                    if datetime.now().date()== adv.date_end:
                        adv.delete()

                shop_advertised = None
                if idss:
                    random_ids = random.choice(idss)
                    shop_advertised=Shop.objects.filter(ids=random_ids).first()
                return render(request, 'SelectRole.html',
                              {'name': account.name, 'idc': account.idc, 'idso': account.idso, 'shop':shop_advertised})
            except Account.DoesNotExist:
                error = 'Inserted data are not valid'
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
    idso = request.session.get('idso', '')
    shops = Shop.objects.filter(idso='idso').values()
    return render(request, 'account_list.html', {'shops': shops, 'idso': idso})
    # account = Account.objects.all()
    # return render(request, 'account_list.html', {'account': account})


# CUSTOMER
def Customer_view(request):
    idc  = request.session.get('idc', '')
    account = Account.objects.filter(idc=idc).first()
    return render(request, 'Customer.html', {'customer': account})


# CUSTOMER Booking
def Customer_CategorySelection_view(request):
    Category_form = forms.ShopCategorySelectionForm()
    if request.method == 'POST':
        selected_category = request.POST.get('category')
        return redirect('Booking_view', selected_category)

    return render(request, 'CustomerCategorySelection.html')


def Booking_view(request, selected_category):
    #Loading of the Django forms into variables
    Shop_and_day_form = forms.Shop_and_day_selectionForm()
    TimeSlot_form = forms.TimeSlot_selectionForm()

    #Filtering of the shops based on the category that the customer has selected in the previous view
    shops = Shop.objects.filter(category=selected_category)

    queues = []
    reviews = []

    for shop in shops:
        timeslot1 = TimeSlot.objects.filter(shop=shop)
        num_av_slots, _, _ = shop.checkQueue(timeslot1)
        shop.queue = num_av_slots + shop.queue_no_app
        shop.save()
        queues.append(shop.queue)
        reviews.append(shop.rating)




    addresses = [shop.address for shop in shops]
    names = [shop.name for shop in shops]

    print(addresses)
    print(names)
    print(queues)
    print(reviews)

    #Condition that verifies if form is sent
    if request.method == 'POST':

        #Condition that verifies if the first form is sent, thus the one of the shop selection to inspect its time slots
        if 'btnform1' in request.POST:
            # Recover the information of the selected shop and date
            shop_ids = request.POST.get('shop_ids')
            date = request.POST.get('date')
            #Finding out the associeted objects
            shop = Shop.objects.get(ids=shop_ids)
            timeslots = TimeSlot.objects.filter(shop=shop, date=date, available=True)
            names = [shop.name for shop in shops]
            return render(request, 'booking.html',
                          {'shops': Shop.objects.filter(category=selected_category),
                           'timeslots': timeslots,
                           'Shop_and_day_form': Shop_and_day_form, 'TimeSlot_form': TimeSlot_form,
                           'addresses': addresses, 'names': names, 'queues': queues,
                            'reviews': reviews})

        if 'btnform2' in request.POST and 'selected_slot' in request.POST:
            #Recovering the information of the actual customer of its selected time slot
            idc = request.session.get('idc', '')
            selected_timeslot_id = request.POST.get('selected_slot')
            #Identification of the associated timeslot object, its slots and its associeted shop
            timeslot = get_object_or_404(TimeSlot, id=selected_timeslot_id)
            
            slot = Slot.objects.filter(TimeSlot=timeslot, available=True).first()            
            shop = timeslot.shop
            #Making the reservation for the customer: association of the slot to him and the slot is now unavailable
            slot.available = False
            slot.idc = idc
            slot.save()
            
            #Checking if the availability of the time slot: if all of the slots are unavailable, the it is also their timeslot 
            if not Slot.objects.filter(available=True, TimeSlot=timeslot).exists():
                timeslot.available = False
                timeslot.save()

            #Creation of the QR to keep track of the reservation and rendering of its html webpage
            qr_data = f"Negozio: {shop.ids}\nData: {timeslot.date}\nOrario: {timeslot.start} - {timeslot.end}\nNumero nella fscia oraria: {slot.number}\nIdc: {slot.idc}"

            qr_code_img = qrcode.QRCode()
            qr_code_img.add_data(qr_data)
            qr_code_img.make(fit=True)

            image = qr_code_img.make_image(fill="black", back_color="white")
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            buffer.seek(0)
            qr_code_img_str = base64.b64encode(buffer.read()).decode('utf-8')
            addresses = [shop.address for shop in Shop.objects.all()]

            idQR = str(uuid.uuid4())
            qr = QR(img=qr_code_img_str, idc=slot.idc, idso=shop.idso, ids=shop.ids, idQR=idQR, number=slot.number,
                    date=timeslot.date, time_start=timeslot.start, time_end=timeslot.end)
            qr.save()

            context3={'qr_code_img': qr_code_img_str,
                      'shop': Shop.objects.filter(category=selected_category).values(),
                      'QR': qr, 'addresses': addresses,
                      'Shop_and_day_form': Shop_and_day_form,
                       'TimeSlot_form': TimeSlot_form}

            return render(request, 'qr.html',context=context3)


    context1 = {
        'shops': shops,
        'Shop_and_day_form': Shop_and_day_form,
        'TimeSlot_form': TimeSlot_form,
        'addresses': addresses,
        'names': names,
        'queues': queues,
        'reviews': reviews,
    }


    return render(request, 'booking.html', context=context1)


# CUSTOMER reservations

def Reservation_view(request):
    idc = request.session.get('idc', '')
    qrs = QR.objects.filter(idc=idc)
    print(qrs)
    shop_names = []
    shop_address = []

    for qr in qrs:
        shop = Shop.objects.get(ids=qr.ids)

        shop_names.append(shop.name)
        shop_address.append(shop.address)


    if (request.GET.get('Guide')):
        ids_for_address = request.GET.get('ids')
        shop_for_address = Shop.objects.get(ids=ids_for_address)
        address=shop_for_address.address
        maps_url = f"https://www.google.com/maps/search/?api=1&query={address}"

        return redirect(maps_url)
    
    if (request.GET.get('Delete_QR')):
        QR_to_delete = get_object_or_404(QR, idQR=request.GET.get('idQR'))

        return redirect('DeleteQR', idQR=QR_to_delete.idQR)

    list = zip(qrs , shop_names, shop_address)

    context = {
        'list':list
    }

    return render(request, 'CustomerReservations.html',context=context)

def DeleteQR(request, idQR):
    qr = get_object_or_404(QR, idQR=idQR)
    if (request.GET.get('Choice')):
        Choice = request.GET.get('Choice')
        if Choice == 'Yes':
            start = qr.time_start
            end = qr.time_end
            date = qr.date
            shop=get_object_or_404(Shop, ids=qr.ids)
            slot = Slot.objects.filter(number=qr.number, available=False, TimeSlot__start=start, TimeSlot__end=end, TimeSlot__date=date, TimeSlot__shop=shop, idc=request.session.get('idc', ))[:1].get()
            slot.available = True
            slot.save()
            qr.delete()

        return redirect('Reservation_view')

    return render(request, 'DeleteQR.html')



def write_review(request):
    idc = request.session.get('idc', '')
    reviews = Review.objects.filter(written=False, idc=idc)
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        rating = int(request.POST.get(f'rating_{review_id}'))
        review = Review.objects.get(id=review_id)
        shop = review.ids
        shop.rating = round(((shop.rating * shop.num_reviews) + rating) / (shop.num_reviews + 1), 1)
        shop.num_reviews += 1
        shop.save()
        review.written = True
        review.save()

    return render(request, "Reviews.html", {'reviews': reviews})


# SHOP OWNER
def ShopOwner_view(request):
    return render(request, 'ShopOwner.html')


def Shop_view(request):
    
    #Condition on the form reception with the data of the shop
    if request.method == 'POST':
        #Creation of the object related with the shop
        form = ShopForm(request.POST, request.FILES)
        #Condition on the form validity
        if form.is_valid():
            #Saving the different fields provided by the form
            
            name = form.cleaned_data['name']
            lat = form.cleaned_data['lat']
            lon = form.cleaned_data['lon']
            max_numb_clients = form.cleaned_data['max_numb_clients']
            address_form = form.cleaned_data['address']
            number  = form.cleaned_data['number']
            cap = form.cleaned_data['CAP']
            city = form.cleaned_data['City']
            category = form.cleaned_data['category']
            opening_time = form.cleaned_data['opening_time']
            closing_time = form.cleaned_data['closing_time']
            if opening_time > closing_time:
                return render(request, 'ErrorTimeShop.html')
                
            slot_duration = form.cleaned_data['slot_duration']

            address= address_form + " " + number + " "+ cap + " " + city
            #Identification of the shop owner 
            idso = request.session.get('idso', '')

            ids = str(uuid.uuid4())

            #Creation of the object shop
            shop = Shop(name=name, lat=lat, lon=lon, max_numb_clients=max_numb_clients, ids=ids, idso=idso,
                        address=address, rating=0, num_reviews=0, category=category)

            # assegnare il campo immagine dell'istanza di Shop al file caricato dall'utente
            
             #Condition to check if the shop owner has loaded an image for his shop
            if 'img' in request.FILES:
                shop.img = request.FILES['img']

            #Saving of the object shop in the database
            shop.save()

            #Creation of the timslots: they will be defined from a year starting from now
            slot_duration = timedelta(minutes=slot_duration)

            current_date = datetime.now().date()
            end_date = current_date + timedelta(weeks=52)  # time slots definiti per un anno


            # SE ABBIAMO tempo creare per giorni diversi ls possibilità di inserire time slots diversi
            #Loop while on the date: it continues if the actual date is not exceeding the ending date
            while current_date <= end_date:
                #Checking if the week day is not in the week-end (Actually the time slots can be defined only during the week days and not during the weekend)
                if current_date.weekday() < 5:
                    current_datetime = datetime.combine(current_date, opening_time)

                    #Loop while on the time of the actual date: it continues if the actual time is not exceeding the closing time
                    while current_datetime.time() < closing_time:
                        #Creation of the time slot
                        date = current_datetime.date()
                        start_time = current_datetime.time()
                        end_time = min(current_datetime + slot_duration,
                                       datetime.combine(current_date, closing_time)).time()

                        time_slot = TimeSlot(start=start_time, end=end_time, date=date, available=True, shop=shop)
                        time_slot.save()
                        
                        #Creation of the slots in the TimeSlot
                        for i in range(1, shop.max_numb_clients+1):
                            slot = Slot(number=i, available=True, TimeSlot=time_slot)
                            slot.save()
                        
                        #Updating of the time in the date
                        current_datetime += slot_duration

                #Updating of the date
                current_date += timedelta(days=1)
 

            return redirect('SuccessShopRegistration')

    else:
        form = ShopForm()

    return render(request, 'ShopRegistration.html')


def SuccessShopRegistration(request):
    return render(request, 'registrationShopSuccess.html')


def MyShops_view(request, ):
    idso = request.session.get('idso', '')
    shops = Shop.objects.filter(idso=idso)

    idcs = []

    # Queue update
    for shop in shops:
        #Prendo tutti i timeslot associati allo shop
        timeslot = TimeSlot.objects.filter(shop=shop)
        #Individuo il numero di persone in coda attualmente
        num_av_slots, _, _ = shop.checkQueue(timeslot)
        shop.queue = num_av_slots + shop.queue_no_app
        shop.save()

    #Advertisement
    adv=[]
    for shop in shops:
        advert = Advertisement.objects.filter(ids=shop.ids).first()
        if advert:
            adv.append(advert)
        else:
            adv.append(None)

    context = {
        'list': zip(shops, adv),
        'idcs': idcs
    }

    if (request.GET.get('ADDbtn')):
        shop = get_object_or_404(Shop, ids=request.GET.get('ShopIDs'))
        shop.queue_no_app += 1
        shop.save()
        return redirect('MyShops_view')

    if (request.GET.get('DECbtn')):
        shop = get_object_or_404(Shop, ids=request.GET.get('ShopIDs'))
        if (shop.queue_no_app > 0):
            shop.queue_no_app -= 1
            shop.save()
        return redirect('MyShops_view')

    if (request.GET.get('SCANbtn')):
        shop = get_object_or_404(Shop, ids=request.GET.get('ShopIDs'))
        timeslot = TimeSlot.objects.filter(shop=shop)
        _, accounts, _ = shop.checkQueue(timeslot)
        context['accounts'] = accounts
        return render(request, 'MyShops.html', context=context)

    if (request.GET.get('Delete_shop')):
        shop_to_delete = get_object_or_404(Shop, ids=request.GET.get('ShopIDs'))
        return redirect('DeleteShop', ids=shop_to_delete.ids)

    if (request.GET.get('QueueList')):
        shop_to_show_queue = get_object_or_404(Shop, ids=request.GET.get('ShopIDs'))
        return redirect('ShopQueueList', ids=shop_to_show_queue.ids)

    if (request.GET.get('Delete_adv')):
        adv_to_delete = get_object_or_404(Advertisement, ids=request.GET.get('ShopIDs'))
        return redirect('DeleteAdv', ids=adv_to_delete.ids)

    if request.GET.get('Obtained'):
        idc = request.GET.get('customer')
        print(idc)
        return redirect('Scan_product', idc=idc)

    return render(request, 'MyShops.html', context=context)

def ShopQueueList(request, ids):
    shop = get_object_or_404(Shop, ids=ids)
    #Trovo tutti i timeslot associati allo shop
    timeslot = TimeSlot.objects.filter(shop=shop)
    #customers sono gli idc dei clienti attualmente in coda; actual_timeslot è il timeslot attuale
    _, customers, actual_timeslot = shop.checkQueue(timeslot)

    qrs=[]
    names=[]

    if customers:
        # ottengo una lista di customers univoca (quando si fa filter per idc_cust, vengono ridate tutte le prenotazioni di un customer)
        unique_customers = set(customers)  

        for cust in unique_customers:
            idc_cust=cust.idc

            qr  =  QR.objects.filter(ids=ids, idso=request.session.get('idso', ), idc=idc_cust,time_start=actual_timeslot.start, time_end=actual_timeslot.end, scanned=False)
            qrs.extend(qr)
        
        # ordinamento della lista qrs in base all'attributo 'number'
        qrs = sorted(qrs, key=lambda x: x.number)

        # ottengo una lista di nomi (quando si fa filter per cust.idc, il nome ridato è univoco)
        for qr in qrs:
            name = Account.objects.filter(idc=qr.idc).first()
            if name:
                names.append(name.name)  

    #print(qrs)
    #print(names)
        

    numberNOAPP=[]
    if shop.queue_no_app>=0:
        for i in range(shop.queue_no_app):
            numberNOAPP.append(shop.max_numb_clients+i+1)
    # if (request.GET.get('Choice')):
    #     Choice = request.GET.get('Choice')
    #     if Choice == 'Yes':
    #         shop.delete()

        # return redirect('MyShops_view')

    list = zip(qrs ,names)

    context = {
        'list':list,
        'NumberNOAPP': numberNOAPP,
        'shop': shop
    }

    return render(request, 'ShopQueueList.html', context=context)


def DeleteShop(request, ids):
    shop = get_object_or_404(Shop, ids=ids)
    if (request.GET.get('Choice')):
        Choice = request.GET.get('Choice')
        if Choice == 'Yes':
            #Delete of the QRs associeted to the shop
            for qr in QR.objects.filter(ids=shop.ids):
                qr.delete()
            #Delete of the advertisement associeted to the shop
            for adv in Advertisement.objects.filter(ids=shop.ids):
                adv.delete()  
            shop.delete()

        return redirect('MyShops_view')

    return render(request, 'DeleteShop.html')

def DeleteAdv(request, ids):
    adv = get_object_or_404(Advertisement, ids=ids)
    if (request.GET.get('Choice')):
        Choice = request.GET.get('Choice')
        if Choice == 'Yes':
            adv.delete()

        return redirect('MyShops_view')

    return render(request, 'DeleteAdvertisement.html')


def Product_view(request):
    Product_form = forms.ProductForm()
    selected_shop = 0
    idso = request.session.get('idso', '')
    if request.method == 'POST':
        shops = Shop.objects.filter(idso=idso).values()
        ids_selected_shop = request.POST.get('selected_shop')
        shop_id = Shop.objects.get(ids=ids_selected_shop)
        request.session['ids'] = str(shop_id.ids)
        product_name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        shop_discount = request.POST.get('shop_discount')
        idso = request.session.get('idso', '')
        ids = request.session.get('ids', '')
        idp = str(uuid.uuid4())

        qr_data = f"Prodotto: {idp}\nNome: {product_name}\nPrice: {price}\nDiscount: {shop_discount}\nQuantity: {quantity}"

        qr_code_img = qrcode.QRCode()
        qr_code_img.add_data(qr_data)
        qr_code_img.make(fit=True)

        image = qr_code_img.make_image(fill="black", back_color="white")
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)
        qr_code_img_str = base64.b64encode(buffer.read()).decode('utf-8')

        product = Product(name=product_name, price=price, shop_discount=shop_discount, idso=idso, ids=ids, idp=idp,
                          quantity=quantity, qr=qr_code_img_str)
        product.save()

        return redirect('SuccessProductRegistration')

    context = {

        'shops': Shop.objects.filter(idso=idso),
        'Product_form': Product_form,
        'selected_shop': selected_shop,
    }
    return render(request, 'ProductRegistration.html', context=context)


def SuccessProductRegistration(request):
    return render(request, 'registrationProductSuccess.html')


def Advertisement_view(request):
    idso = request.session.get('idso', '')
    shops=Shop.objects.filter(idso=idso)

    #Removing of the aldready advertised shops
    shopadvlist=[]
    for shop in shops:
        Adv=Advertisement.objects.filter(ids=shop.ids)
        if Adv:
            shopadvlist.append(shop)
    
    # Rimozione degli shop pubblicizzati dalla lista degli shop
    shops_not_adv_yet = [shop for shop in shops if shop not in shopadvlist]


    

    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            ids_selected_shop = request.POST.get('selected_shop')
            starting_date = datetime.now().date()
            period = int(request.POST.get('period'))
            ending_date = starting_date + relativedelta(months=period)
            ida = str(uuid.uuid4())
            adv = Advertisement(date_start= starting_date, date_end= ending_date, ADVid=ida, ids=ids_selected_shop)
            adv.save()
            return redirect('SuccessAdvertisementRegistration', ids=ids_selected_shop)

    context = {

        'shops': shops_not_adv_yet
    }
    return render(request, 'Advertisement.html',  context=context)

def SuccessAdvertisementRegistration(request, ids):
    adv = get_object_or_404(Advertisement, ids=ids)

    context = {

        'date': adv.date_end

    }
    return render(request, 'registrationAdvertisementSuccess.html',context=context)




# def booking(request):
# if request.method == 'POST':
#   shop_name = request.POST.get('shop_name')
#  date = request.POST.get('date')
# Store shop name and date in django session:
# request.session['shop_name'] = shop_name
# request.session['date'] = date

# return redirect('bookingSubmit')

# return render(request, 'booking.html', {'shops': Shop.objects.filter(category='booking').values()})


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
# def Customer_category_view(request):
# Category_form = forms.ShopCategorySelectionForm()
# if request.method == 'POST':
#   selected_category = request.POST.get('category')
#   shop = Shop.objects.filter(category=selected_category).values()
# return render(request, 'category_selection.html', {'shop': shop})


def scan_qr(request):
    if request.method == 'POST':
        qr_code_value = request.POST.get('qrCodeValue')

        qr_code_lines = qr_code_value.split('\n')
        ids = qr_code_lines[0].split(': ')[1]
        ids = ids.strip()
        date_str = qr_code_lines[1].split(': ')[1]
        date_str = date_str.strip()
        time_range_str = qr_code_lines[2].split(': ')[1]
        time_range_str = time_range_str.strip()
        number_within_slot = qr_code_lines[3].split(': ')[1]
        number_within_slot = number_within_slot.strip()
        idc = qr_code_lines[4].split(': ')[1]
        idc = idc.strip()

        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        start_time_str, end_time_str = time_range_str.split(' - ')
        start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
        end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()

        start_datetime = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)

        if end_datetime < datetime.now():
            return render(request, 'Expired_qr_code.html')

        # da fare il get con l'ids!!!
        try:
            shop = Shop.objects.get(ids=ids)
        except Shop.DoesNotExist:
            return render(request, 'error.html')

        try:
            time_slot = TimeSlot.objects.get(shop=shop, start=start_datetime, end=end_datetime, date=date)
            slot = Slot.objects.get(TimeSlot=time_slot, number=number_within_slot)
            if not slot.available:
                qr = QR.objects.get(ids=ids, date=date, time_start=start_datetime, time_end=end_datetime,
                                    number=number_within_slot)
                qr.scanned = True
                qr.delete()
                review = Review(ids=shop, idc=idc, name_of_the_shop=shop.name)
                review.save()
                return render(request, "scan_successful.html", {'review': review})
        except TimeSlot.DoesNotExist:
            return render(request, 'error.html')

    return render(request, 'scan.html')


def Scan_product(request, idc):
    if request.method == 'GET':
        return render(request, 'Scan_product.html', {'idc': idc})

    if request.method == 'POST':
        idc = request.session.get('idc', '')
        customer = Account.objects.get(idc=idc)
        qr_code_value = request.POST.get('qrCodeValue')
        qr_code_lines = qr_code_value.split('\n')
        idp = qr_code_lines[0].split(': ')[1]
        idp = idp.strip()
        name = qr_code_lines[1].split(': ')[1]
        name = name.strip()
        price = qr_code_lines[2].split(': ')[1]
        price = price.strip()
        shop_discount = qr_code_lines[3].split(': ')[1]
        shop_discount = shop_discount.strip()
        quantity = qr_code_lines[4].split(': ')[1]
        quantity = quantity.strip()

        product = Product.objects.get(idp=idp)
        account = Account.objects.get(idc=idc)
        purchase_list = PurchaseList.objects.get(idc=account)

        product.quantity -= 1
        customer.reward += price
        customer.save()

        if product.quantity == 0:
            product.delete()
            return render(request, "Products are over.html")

        product.save()

        purchased_item = PurchasedItem(purchase_list=purchase_list, idp=idp, name=product.name)
        purchased_item.save()

        return render(request, "scan_successful_purchase.html", )


def Purchase_list(request):
    idc = request.session.get('idc', '')
    account = Account.objects.get(idc=idc)
    purchase_list = PurchaseList.objects.get(idc=account)

    items = PurchasedItem.objects.filter(purchase_list=purchase_list)
    name_shops = []
    address_shops = []
    prices = []

    for item in items:
        product = get_object_or_404(Product, idp=item.idp)
        shop = get_object_or_404(Shop, ids=product.ids)
        name_shops.append(shop)
        address_shops.append(shop.address)
        prices.append(product.price)

    list = zip(items, name_shops, address_shops, prices)

    return render(request, "Purchase_list.html", context={'list': list})


def QR_print(request):
    idso = request.session.get('idso', '')
    products = Product.objects.filter(idso=idso)
    return render(request, "QR_print.html", {'products': products})


def Wish_list(request):
    idc = request.session.get('idc', '')
    idc = Account.objects.get(idc=idc)
    wishlist = WishList.objects.get(idc=idc)
    items = WishListItem.objects.filter(wish_list=wishlist)
    name_shops = []
    address_shops = []
    prods = []
    prices = []
    itemss = []
    for item in items:
        product = get_object_or_404(Product, idp=item.idp)
        shop = get_object_or_404(Shop, ids=product.ids)
        name_shops.append(shop)
        address_shops.append(shop.address)
        prods.append(item.name)
        prices.append(product.price)
        itemss.append(item)

    list = zip(prods, address_shops, name_shops, prices, itemss)

    similar_products = None
    show_search_bar = False
    data = []

    if request.method == 'POST':
        if 'Remove' in request.POST:
            product_idp = request.POST.get('product_idp')
            print(product_idp)
            # Cancella tutti gli elementi associati a questo ID prodotto
            WishListItem.objects.filter(idp=product_idp).delete()
            return redirect('WishList')

        if 'add_products' in request.POST:
            show_search_bar = True
        elif 'query' in request.POST:
            query = request.POST['query']
            terms = query.split()

            similar_products = []
            names = []
            addresses = []
            for term in terms:
                term = term.strip()
                try:
                    item = Product.objects.get(name=term)
                    similar_products.append(item)
                    shop_id = item.ids
                    shop_obj = Shop.objects.get(ids=shop_id)
                    name = shop_obj.name
                    names.append(name)
                    address = shop_obj.address
                    addresses.append(address)
                except Product.DoesNotExist:
                    continue

            data = zip(similar_products, names, addresses)

        elif 'selected_product' in request.POST:
            selected_product_id = request.POST['selected_product']

            product = Product.objects.get(idp=selected_product_id)

            new = WishListItem(idp=product.idp, name=product.name, wish_list=wishlist)
            new.save()
            return redirect('WishList')

    return render(request, "WishList.html", {'list': list, 'show_search_bar': show_search_bar,
                                             'similar_products': similar_products, 'data': data})
