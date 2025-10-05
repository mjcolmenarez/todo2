#Routes for the to-do app
from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    #The main list page with filters and sorting 
    path("", views.list_view, name="list"),
    #New task form
    path("new/", views.create_view, name="create"),
    #Update an existing task
    path("edit/<int:pk>/", views.update_view, name="edit"),
    #Confirm and delete a task
    path("delete/<int:pk>/", views.delete_view, name="delete"),
    #One-click flip between done/undone
    path("toggle/<int:pk>/", views.toggle, name="toggle"),
    #Columns for to-do/doing/done
    path("kanban/", views.kanban_view, name="kanban"),
    #Download a CSV of the current list
    path("export/", views.export_csv, name="export"),
]
