from django.shortcuts import render

# render method takes 2 parameter and 2 optional: 1 is the HTTP request and other is the template

rooms = [
    { 'id': 1, 'name': 'Lets learn Django' },
    { 'id': 2, 'name': 'Design with me' },
    { 'id': 3, 'name': 'Frontend Developers' }
]

def home(request):
    context = {'rooms': rooms} # here we are getting all dictionaries in a list
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i # here room will be equal to id, as in the urls.py room/<pk> == room/id
    context = {'room': room} # here we are getting each single room according to it's id i.e each single dictionary
        
    return render(request, 'base/room.html', context)