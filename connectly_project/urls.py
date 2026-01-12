from django.contrib import admin
from django.urls import path, include  # include is required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),  # include the posts app URLs
]