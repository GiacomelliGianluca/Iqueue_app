# Create your models here.
from django.db import models
from django.core.validators import MinLengthValidator
from datetime import date, datetime
from datetime import time


# Realizziamo tutti gli ID di lunghezza 8


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


class Shop(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField(default=0)  # latitude
    lon = models.FloatField(default=0)  # longitude
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
        current_time = datetime.now().time()
        current_date = datetime.now().date()

        forced_date = datetime(2023, 6, 22).date()
        forced_time = datetime(2023, 6, 21, 8, 30).time()

        # forced_datetime = datetime.combine(forced_date, forced_time)

        timeslot = timeslots.filter(shop=self, date=forced_date, start__lte=forced_time, end__gt=forced_time).first()

        if timeslot:
            # Conta il numero di slot disponibili per il timeslot attuale
            num_available_slots = Slot.objects.filter(TimeSlot=timeslot, available=False).count()

            # Ottieni gli idc dei timeslot attuali
            idcs = Slot.objects.filter(TimeSlot=timeslot, available=False).values_list('idc', flat=True)


            return num_available_slots, idcs
        return 0, []



class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    shop_discount = models.FloatField()
    idso = models.CharField(default='OOOOOOOO', max_length=36, validators=[MinLengthValidator(8)])
    ids = models.CharField(default='SSSSSSSS', max_length=36, validators=[MinLengthValidator(8)])
    idp = models.CharField(default='PPPPPPPP', max_length=36, validators=[MinLengthValidator(8)])
    # shop = models.ForeignKey(Shop, on_delete=models.CASCADE, default='0')


class TimeSlot(models.Model):
    start = models.TimeField()
    end = models.TimeField()
    date = models.DateField(default=date.today)
    available = models.BooleanField(default=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)


class Slot(models.Model):
    number = models.IntegerField(default=1)
    available = models.BooleanField(default=True)
    TimeSlot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, blank=True, null=True)
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


# class QR(models.Model):   #Vedere se mettere campi come gli altri
#     QRid = models.CharField(max_length=50)
#     ids = Shop.ids
#     idso = Shop_owner.idso
#     idc = Customer.idc

class Review(models.Model):
    review = models.TextField(default="")
    date = models.DateField(default=date.today)
    idc = models.CharField(max_length=36, validators=[MinLengthValidator(8)])
    ids = models.ForeignKey(Shop, on_delete=models.CASCADE, )
    name_of_the_shop = models.CharField(max_length=36, default='SSSSSSSSSSSSSSS', validators=[MinLengthValidator(8)])
    written = models.BooleanField(default=False)
