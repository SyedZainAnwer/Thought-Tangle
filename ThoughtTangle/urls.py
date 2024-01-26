from django.contrib import admin
from django.urls import path, include

# urls trigger views and that what we see on the server
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')), # any path that matches and empty string, go to base.urls file
    path('api/', include('base.api.urls'))
]
