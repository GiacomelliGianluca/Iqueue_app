from django import forms


class RegistrationForm(forms.Form):
    first_name = forms.CharField(label='name')
    last_name = forms.CharField(label='surname')
    password = forms.CharField(widget=forms.PasswordInput, label='password')
    email = forms.EmailField(label='email')
    birthday = forms.DateField()

class RegistrationForm_fromLogIN(forms.Form):
    check = forms.BooleanField()  #campo che dovrebbe essere inutile (è definito solo per non far dar problemi alla classe)


class LogIn(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label='password')
    email = forms.EmailField(label='email')
 

class ShopForm(forms.Form):
    name = forms.CharField(label='name')
    location = forms.CharField(label='location')
    max_numb_clients = forms.IntegerField(label='max_numb_clients')
    ids = forms.CharField(label='ids')
    address = forms.CharField(label='address')
    category = forms.CharField(label='category')