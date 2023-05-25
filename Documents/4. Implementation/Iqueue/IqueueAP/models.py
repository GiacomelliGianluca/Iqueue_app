# Create your models here.
from django.db import models
from django.core.validators import MinLengthValidator
from datetime import date


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
    ids = models.CharField(default='SSSSSSSS', max_length=36, validators=[MinLengthValidator(8)])
    address = models.CharField(max_length=200)
    rating = models.FloatField(default=0)
    numb_of_ratings = models.IntegerField(default=0)
    category = models.CharField(max_length=100, default='Others')  # Se non compilato messo in others
    idso = models.CharField(default='SSSSSSSS', max_length=36, validators=[MinLengthValidator(8)])


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    shop_discount = models.FloatField()
    idso = models.CharField(default='SSSSSSSS', max_length=36, validators=[MinLengthValidator(8)])
    ids = models.CharField(default='SSSSSSSS', max_length=36, validators=[MinLengthValidator(8)])
    idp = models.CharField(default='SSSSSSSS', max_length=36, validators=[MinLengthValidator(8)])
    #shop = models.ForeignKey(Shop, on_delete=models.CASCADE, default='0')


class TimeSlot(models.Model):
    start = models.TimeField()
    end = models.TimeField()
    date = models.DateField(default=date.today)
    available = models.BooleanField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)


# Vedere se togliere
TIME_CHOICES = (
    ("3 PM", "3 PM"),
    ("3:30 PM", "3:30 PM"),
    ("4 PM", "4 PM"),
    ("4:30 PM", "4:30 PM"),
    ("5 PM", "5 PM"),
    ("5:30 PM", "5:30 PM"),
    ("6 PM", "6 PM"),
    ("6:30 PM", "6:30 PM"),
    ("7 PM", "7 PM"),
    ("7:30 PM", "7:30 PM"),
)


class Booking(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(default=date.today)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="3 PM")

# class QR(models.Model):   #Vedere se mettere campi come gli altri
#     QRid = models.CharField(max_length=50)
#     ids = Shop.ids
#     idso = Shop_owner.idso
#     idc = Customer.idc
