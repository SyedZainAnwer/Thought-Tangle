from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm

# render method takes 2 parameter and 2 optional: 1 is the HTTP request and other is the template

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    ) # query for room. we are gonna search by these queries
    
    topics = Topic.objects.all()
    room_count = rooms.count()
    
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count} # here we are getting all dictionaries in a list
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room} # here we are getting each single room according to it's id i.e each single dictionary
        
    return render(request, 'base/room.html', context)

# function to create a new Room
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

# function to update/edit specific room
def updateRoom(request, pk):
    room = Room.objects.get(id=pk) # fetching the data of the specific room by its ID
    form = RoomForm(instance=room) # creating the RoomForm for that fetched room. instance keyword let the form being pre-filled with the existing data that the room had
    
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    # another way to do that:
    # room = get_object_or_404(Room, id=pk)
    
    if request.method == "POST":
        room.delete()
        return redirect('home')
    
    context = { 'obj': room }
    return render(request, 'base/delete.html', context)