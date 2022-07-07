from django.urls import path

from . import views

app_name = 'wiki'

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search/<str:title>", views.search_similar, name="search"),
    path("new", views.new, name="new")
]
