# Create your models here.
from django.db import models
from django.core.validators import MinLengthValidator

#Realizziamo tutti gli ID di lunghezza 8

class Coordinates(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()


class Account(models.Model): #La classe account corrisponde a user di UML
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    birthday = models.DateField()

    def user_login(self, email: str, password: str):
        self.email = email
        self.password = password



# #Vedere se i campi "inherited" servono tutti/ha senso inglobarli tutti (Io ho fatto così per definizione subclass)
# class Customer(models.Model):
#     name = models.OneToOneField(Account, on_delete = models.CASCADE)
#     surname = models.OneToOneField(Account, on_delete = models.CASCADE)
#     password = models.OneToOneField(Account, on_delete = models.CASCADE)
#     email = models.OneToOneField(Account, on_delete = models.CASCADE)
#     birthday = models.OneToOneField(Account, on_delete = models.CASCADE)
#     idc = models.CharField(default='CCCCCCCC',max_length=8, validators=[MinLengthValidator(8)])
#     lat = Coordinates.latitude                                                                       #latitude
#     lon = Coordinates.longitude                                                                      #longitude
#     reward = models.IntegerField(default=0)
    

# class Shop_owner(models.Model):
#     name = models.OneToOneField(Account, on_delete = models.CASCADE)
#     surname = models.OneToOneField(Account, on_delete = models.CASCADE)
#     password = models.OneToOneField(Account, on_delete = models.CASCADE)
#     email = models.OneToOneField(Account, on_delete = models.CASCADE)
#     birthday = models.OneToOneField(Account, on_delete = models.CASCADE)  
#     idso = models.CharField(default='OOOOOOOO',max_length=8, validators=[MinLengthValidator(8)])
#     lat = Coordinates.latitude                                                                       #latitude
#     lon = Coordinates.longitude                                                                      #longitude
#     reward = models.IntegerField(default=0)
#     on_delete = models.CASCADE


class Shop(models.Model):
    name = models.CharField(max_length=100)
    lat = Coordinates.latitude                                                                       #latitude
    lon = Coordinates.longitude                                                                      #longitude
    max_numb_clients = models.IntegerField()
    queue = models.IntegerField(default=0)
    ids = models.CharField(default='SSSSSSSS',max_length=8, validators=[MinLengthValidator(8)])
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

# class QR(models.Model):   #Vedere se mettere campi come gli altri
#     QRid = models.CharField(max_length=50)
#     ids = Shop.ids
#     idso = Shop_owner.idso
#     idc = Customer.idc


