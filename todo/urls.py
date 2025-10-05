#This is the map of the system
from django.contrib import admin
from django.urls import path, include

#If a path starts with "admin/", send it to Django admin
#Everything else goes to our tasks app (see tasks/urls.py for the details)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("tasks.urls", "tasks"), namespace="tasks")),
]
