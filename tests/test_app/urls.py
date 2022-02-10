from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("/", TemplateView.as_view(template_name="app.html"), name="test"),
    path("home/", views.home, name="home"),
]
