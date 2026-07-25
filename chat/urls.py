from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("chat/<str:username>/", views.chat_view, name="chat"),

    # Admin Dashboard
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
