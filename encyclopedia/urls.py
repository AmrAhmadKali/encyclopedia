from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("create", views.new_page, name="new_page"),
    path("edit<str:title>", views.edit, name="edit"),
    path("random", views.random, name="random"),
    path("<str:title>", views.entry, name="entry")
]
