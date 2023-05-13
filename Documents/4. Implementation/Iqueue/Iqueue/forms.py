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
 

class ShopForm(forms.Form):
    name = forms.CharField(label='name')
    lat = forms.CharField(label='latitude')
    lon = forms.CharField(label='longitude')
    max_numb_clients = forms.IntegerField(label='max_numb_clients')
    ids = forms.CharField(label='ids')
    address = forms.CharField(label='address')
    category = forms.CharField(label='category')