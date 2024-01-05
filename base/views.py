from django.shortcuts import render
from .models import Room

# render method takes 2 parameter and 2 optional: 1 is the HTTP request and other is the template

def home(request):
    rooms = Room.objects.all() # query for room
    context = {'rooms': rooms} # here we are getting all dictionaries in a list
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room} # here we are getting each single room according to it's id i.e each single dictionary
        
    return render(request, 'base/room.html', context)