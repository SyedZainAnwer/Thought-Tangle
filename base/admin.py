from django.contrib import admin
from .models import Room, Topic, Message

# registering the model Room in admin panel
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)