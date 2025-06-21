from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API routes CRUD
    path("create", views.create, name="create"),
    path("update/<int:post_id>", views.update, name="update"),
    path("read", views.read, name="read"),
    path("delete/<int:post_id>", views.delete, name="delete"),
]
