from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.list_view, name="list"),
    path("new/", views.create_view, name="create"),
    path("edit/<int:pk>/", views.update_view, name="edit"),
    path("delete/<int:pk>/", views.delete_view, name="delete"),
    path("toggle/<int:pk>/", views.toggle, name="toggle"),
    path("kanban/", views.kanban_view, name="kanban"),
    path("export/", views.export_csv, name="export"),
]
