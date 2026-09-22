from django.urls import path

from . import views

app_name = "households"

urlpatterns = [
    path("", views.choose, name="choose"),
    path("create/", views.create, name="create"),
    path("join/", views.join, name="join"),
    path("<int:pk>/", views.detail, name="detail"),
]
