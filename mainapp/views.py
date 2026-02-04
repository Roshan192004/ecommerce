from django.shortcuts import render
from adminapp.models import ServiceableLocation

def home(request):
    location = request.session.get('delivery_location')
    return render(request, 'mainapp/home.html', {
        'location': location
    })
