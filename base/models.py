from django.db import models
from django.contrib.auth.models import User # built-in user class

class Topic(models.Model): # A topic can have multiple rooms, where as room can have 1 topic
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # participants = 
    updated = models.DateTimeField(auto_now=True) # like snapshot on every save of the room
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', '-created'] # here -updated/-created means that the latest created will be at the top and if we remove -, it will be ascending order 
    
    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # One to many relation (a room can have multiple messages. CASCADE deletes all the children in the parent if the parent gets deleted)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.body[0:50] # we want the first 50 characters of the body(message)