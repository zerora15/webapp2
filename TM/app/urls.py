from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("complete/<int:task_id>/", views.complete, name="complete"),
    path("delete/<int:task_id>/", views.delete, name="delete"),
]