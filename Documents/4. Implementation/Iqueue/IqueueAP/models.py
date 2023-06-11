# Create your models here.
from django.db import models
from django.core.validators import MinLengthValidator
from datetime import date, datetime
from datetime import time


class Account(models.Model):  # La classe account corrisponde a user di UML
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    birthday = models.DateField()
    idc = models.CharField(default='CCCCCCCC', max_length=32)  # Solo customer
    lat = models.FloatField(default=0)  # Solo customer    #latitude: da maps
    lon = models.FloatField(default=0)  # Solo customer    #longitude: da maps
    reward = models.IntegerField(default=0)  # Solo customer
    idso = models.CharField(default='OOOOOOOO', max_length=32)  # Solo ShopOwner

    def user_login(self, email: str, password: str):  # Account
        self.email = email
        self.password = password

def get_default_image():
    return "default_image.png"


class Shop(models.Model):
    img = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=10000,  default=get_default_image)
    name = models.CharField(max_length=100)
    max_numb_clients = models.IntegerField()
    queue = models.IntegerField(default=0)
    queue_no_app = models.IntegerField(default=0)
    ids = models.CharField(default='SSSSSSSS', max_length=36, validators=[MinLengthValidator(8)])
    address = models.CharField(max_length=200)
    rating = models.FloatField(default=0)
    num_reviews = models.IntegerField(default=0)
    category = models.CharField(max_length=100, default='Others')  # Se non compilato messo in others
    idso = models.CharField(default='SSSSSSSS', max_length=36, validators=[MinLengthValidator(8)])

    def checkQueue(self, timeslots):
        # current_time = datetime.now().time()
        # current_date = datetime.now().date()
        # timeslot = timeslots.filter(shop=self, date=current_date, start__lte=current_time, end__gt=current_time).first()


        forced_date = datetime(2023, 6, 28).date()
        forced_time = datetime(2023, 6, 28, 8, 30).time()
        timeslot = timeslots.filter(shop=self, date=forced_date, start__lte=forced_time, end__gt=forced_time).first()

        # forced_datetime = datetime.combine(forced_date, forced_time)

        

        if timeslot:
            # Conta il numero di prenotazioni svolte per il timeslot attuale
            QRs_reserved =  QR.objects.filter(time_start=timeslot.start, date=timeslot.date, ids=self.ids)
            num_available_slots = QRs_reserved .count()
            slots_in_time_slot = timeslot.slots.all()
            idc_list = [slot.idc for slot in slots_in_time_slot if slot.idc != ""]
            accounts = []
            for idc in idc_list:
                account = Account.objects.filter(idc=idc)
                accounts.extend(account)

            print(len(accounts))

            return num_available_slots, accounts, timeslot
        
        return 0,None,[]



class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    shop_discount = models.FloatField()
    idso = models.CharField(default='OOOOOOOO', max_length=36, validators=[MinLengthValidator(8)])
    ids = models.CharField(default='SSSSSSSS', max_length=36, validators=[MinLengthValidator(8)])
    idp = models.CharField(default='PPPPPPPP', max_length=36, validators=[MinLengthValidator(8)])
    # shop = models.ForeignKey(Shop, on_delete=models.CASCADE, default='0')
    quantity = models.IntegerField(default=None)
    Available = models.BooleanField(default=True)
    qr = models.TextField(default='')


class TimeSlot(models.Model):
    start = models.TimeField()
    end = models.TimeField()
    date = models.DateField(default=date.today)
    available = models.BooleanField(default=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)


class Slot(models.Model):
    number = models.IntegerField(default=1)
    available = models.BooleanField(default=True)
    TimeSlot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, blank=True, null=True, related_name='slots')
    idc = models.CharField(max_length=36, validators=[MinLengthValidator(8)])


class QR(models.Model):
    img = models.TextField()  # L'immagine è una stringa in base64
    idc = models.CharField(max_length=36, validators=[MinLengthValidator(8)])
    idso = models.CharField(default='OOOOOOOO', max_length=36, validators=[MinLengthValidator(8)])
    ids = models.CharField(default='SSSSSSSS', max_length=36, validators=[MinLengthValidator(8)])
    idQR = models.CharField(default='QQQQQQQQ', max_length=36, validators=[MinLengthValidator(8)])
    number = models.IntegerField(default=-1)  # -1 vuol dire che non è stato ancora assegnato
    date = models.DateField(default=date.today)  # Si compila esso con la stessa data del TimeSlot.date
    time_start = models.TimeField(default=time(0, 0, 0))  # Si compila esso con Timeslot.start
    time_end = models.TimeField(default=time(12, 0, 0))  # Si compila esso con Timeslot.end
    scanned = models.BooleanField(default=False)


class Advertisement(models.Model):
    date_start = models.DateField(default=date.today)
    date_end = models.DateField(default=date.today)
    ADVid = models.CharField(default='AAAAAAAA', max_length=36, validators=[MinLengthValidator(8)])
    ids = models.CharField(default='SSSSSSSS', max_length=36, validators=[MinLengthValidator(8)])


class Review(models.Model):
    review = models.TextField(default="")
    date = models.DateField(default=date.today)
    idc = models.CharField(max_length=36, validators=[MinLengthValidator(8)])
    ids = models.ForeignKey(Shop, on_delete=models.CASCADE, )
    name_of_the_shop = models.CharField(max_length=36, default='SSSSSSSSSSSSSSS', validators=[MinLengthValidator(8)])
    written = models.BooleanField(default=False)


class PurchaseList(models.Model):
    idc = models.ForeignKey(Account, on_delete=models.CASCADE, )


class PurchasedItem(models.Model):
    purchase_list = models.ForeignKey(PurchaseList, on_delete=models.CASCADE, )
    date_of_purchase = models.DateField(default=date.today())
    idp = models.CharField(default="SSSSSSSSSS", max_length=100)
    name = models.CharField(default="SSSSSSSSSS", max_length=100)


class WishList(models.Model):
    idc = models.ForeignKey(Account, on_delete=models.CASCADE, )


class WishListItem(models.Model):
    wish_list = models.ForeignKey(WishList, on_delete=models.CASCADE, )
    idp = models.CharField(default="SSSSSSSSSS", max_length=100)
    name = models.CharField(default="SSSSSSSSSS", max_length=100)
