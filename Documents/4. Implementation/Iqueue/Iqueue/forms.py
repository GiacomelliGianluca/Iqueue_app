from django import forms


class RegistrationForm(forms.Form):
    first_name = forms.CharField(label='name')
    last_name = forms.CharField(label='surname')
    password = forms.CharField(widget=forms.PasswordInput, label='password')
    email = forms.EmailField(label='email')
    birthday = forms.DateField()


class LogIn(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label='password')
    email = forms.EmailField(label='email')
 


CATEGORY_CHOICES = (
        ('bakery', 'Bakery'),
        ('clothes', 'Clothes'),
        ('perfumery', 'Perfumery'),
        ('hair_saloon', 'Hair Saloon'),
        ('others', 'Other'),
    )

class ShopForm(forms.Form):
    name = forms.CharField(label='name')
    lat = forms.FloatField(label='lat')
    lon = forms.FloatField(label='lon')
    max_numb_clients = forms.IntegerField(label='max_numb_clients')
    ids = forms.CharField(label='ids')
    address = forms.CharField(label='address')
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label='category')
