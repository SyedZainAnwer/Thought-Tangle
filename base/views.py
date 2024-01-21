from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm

# render method takes 2 parameter and 2 optional: 1 is the HTTP request and other is the template

def loginPage(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        # these 2 values will be coming from front end
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password does not exist")
    
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request) # this will delete the token from Cookies, which will logout the user
    return redirect(home)


def registerPage(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user) # after registering the user, we logged him in
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration")
    
    context = {'form': form}
    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    ) # query for room. we are gonna search by these queries
    
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)) # we will see only the messages of the related topic in that room
    
    context = { 
            'rooms': rooms, 
            'topics': topics, 
            'room_count': room_count, 
            'room_messages': room_messages 
        } # here we are getting all dictionaries in a list
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all() # we access the child of room (messages) here. It will give us the set of messages that are related to the specific room. Order_by shows the latest messages first. Many to one relation
    participants = room.participants.all() # Many to Many relation
    
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        
        return redirect('room', pk=room.id)
    
    context = {'room': room, 'room_messages': room_messages, "participants": participants} # here we are getting each single room according to it's id i.e each single dictionary

    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all() # for recent activity
    topics = Topic.objects.all()
    
    context= {'user':user, 'rooms': rooms, 'room_messages': room_messages, "topics": topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login') # user cannot create a room until he's logged-in
# function to create a new Room
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user # host will be the logged in user
            room.save()
            return redirect('home')
    
    context = {'form': form, "topics": topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login') # user cannot update a room until he's logged-in
# function to update/edit specific room
def updateRoom(request, pk):
    room = Room.objects.get(id=pk) # fetching the data of the specific room by its ID
    form = RoomForm(instance=room) # creating the RoomForm for that fetched room. instance keyword let the form being pre-filled with the existing data that the room had
    topics = Topic.objects.all()
    
    if request.user != room.host: # it does not allow any other user to edit someones room
        return HttpResponse("You are not allowed here!!")
    
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form, "topics": topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login') # user cannot delete a room until he's logged-in
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    # another way to do that:
    # room = get_object_or_404(Room, id=pk)
    
    if request.user != room.host: # it does not allow any other user to delete someones room
        return HttpResponse("You are not allowed here!!")
    
    if request.method == "POST":
        room.delete()
        return redirect('home')
    
    context = { 'obj': room }
    return render(request, 'base/delete.html', context)


@login_required(login_url='login') # user cannot delete a message until he's logged-in
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse("You are not allowed here!!")
    
    if request.method == "POST":
        message.delete()
        return redirect('home')
    
    context = { 'obj': message }
    return render(request, 'base/delete.html', context)