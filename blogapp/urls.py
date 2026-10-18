from django.urls import path
from . import views
app_name = 'blogapp'
urlpatterns = [
    path("", views.load, name="load"),
    path("new/", views.new, name="new"),
    path("edit/<str:name>", views.edit, name="edit"),
    path("delete/<str:name>", views.delete, name="delete"),
    path("home/", views.home, name="home"),
    path("article/<str:name>", views.article,name="article"),
    path("login/",views.login_view,name="login" ),
    path("logout/",views.logout_view,name="logout"),
]