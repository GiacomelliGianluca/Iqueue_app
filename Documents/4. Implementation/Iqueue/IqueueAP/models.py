# Create your models here.
from django.db import models
from django.core.validators import MinLengthValidator

#Realizziamo tutti gli ID di lunghezza 8

class Account(models.Model): #La classe account corrisponde a user di UML
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    birthday = models.DateField()

    def user_login(self, email: str, password: str):
        self.email = email
        self.password = password

#Vedere come fare
#class customer(Account):  #Da verificare che poi i campi sono inherited correttamente
#    idc = models.CharField(default='BBBBBBBB',max_length=8, validators=[MinLengthValidator(8)])



class QR(models.Model):   #Vedere se mettere campi come gli altri
    QRid = models.CharField(max_length=50)
    ids = models.CharField(max_length=50)
    idso = models.CharField(max_length=50)
    idc = models.CharField(max_length=50)


class Coordinates(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

class Shop(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    max_numb_clients = models.IntegerField()
    queue = models.IntegerField(default=0)
    ids = models.CharField(default='AAAAAAAA',max_length=8, validators=[MinLengthValidator(8)])
    address = models.CharField(max_length=200)
    rating = models.FloatField(default=0)
    numb_of_ratings= models.IntegerField(default=0)
    category = models.CharField(max_length=100, default='Others') #Se non compilato messo in others
    
 

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    shop_discount = models.FloatField()
    id_product = models.CharField(max_length=8, validators=[MinLengthValidator(8)])
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

class TimeSlot(models.Model):
    start = models.TimeField()
    end = models.TimeField()
    available = models.BooleanField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,blank=True, null=True)

