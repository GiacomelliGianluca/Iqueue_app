from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render
from listings.models import Band
from listings.forms import ContactUsForm
from django.core.mail import send_mail


def hello(request):
    return HttpResponse('<h1>Hello Django!</h1>')

def about(request):
    return HttpResponse('<h1>About Us</h1> <p>We love Iqueue</p>')

def bande(request):
    bands = Band.objects.all()
    return render(request, 
                'listings/hello.html',
                {'bands': bands})

def contact(request):
    print('The request method is:', request.method)
    print('The POST data is:', request.POST)
    form = ContactUsForm()
    return render(request,
            'listings/contact.html',
            {'form': form})