from . import views
from django.urls import path


urlpatterns = [
    path('add_produto/', views.add_produto, name="add_produto"),
    path('produto/<slug:slug>', views.produto, name="produto"),
]