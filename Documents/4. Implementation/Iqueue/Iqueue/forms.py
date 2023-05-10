from django import forms


class RegistrationForm(forms.Form):
    first_name = forms.CharField(label='name')
    last_name = forms.CharField(label='surname')
    account_id = forms.CharField(label='id account')
    password = forms.CharField(widget=forms.PasswordInput, label='password')
    email = forms.EmailField(label='email')
    birthday = forms.DateField()


class LogIn(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label='password')
    email = forms.EmailField(label='email')

class ShopForm(forms.Form):
    name = forms.CharField(label='name')
    location = forms.CharField(label='location')
    max_numb_clients = forms.IntegerField(label='max_numb_clients')
    id_shop = forms.CharField(label='id_shop')
    address = forms.CharField(label='address')
    category = forms.CharField(label='category')