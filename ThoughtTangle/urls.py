from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# urls trigger views and that what we see on the server
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')), # any path that matches and empty string, go to base.urls file
    path('api/', include('base.api.urls'))
]

# in 1st param we are setting URL for the image and in 2nd param we are telling it to get the files from this root. This is how we connected MEDIA_URL and MEDIA_ROOT
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
