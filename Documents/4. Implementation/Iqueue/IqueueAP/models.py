# Create your models here.
from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    account_id = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    birthday = models.DateField()

    def user_login(self, email: str, password: str):
        self.email = email
        self.password = password

class TimeSlot(models.Model):
    start = models.TimeField()
    end = models.TimeField()
    available = models.BooleanField()


class QR(models.Model):
    QRid = models.CharField(max_length=50)
    ids = models.CharField(max_length=50)
    idso = models.CharField(max_length=50)
    idc = models.CharField(max_length=50)


class Coordinates(models.Model):
    latitude = models.IntegerField()
    longitude = models.IntegerField()

class Shop(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    max_numb_clients = models.IntegerField()
    id_shop = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    category = models.CharField(max_length=100, default='0000000')
    
 

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    shop_discount = models.FloatField()
    id_product = models.CharField(max_length=50)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)



