from django.urls import path
from . import views

urlpatterns=[
    path("",views.index, name="index"),
    path("cart/",views.carro , name="carro"),
    path("checkout/", views.checkout, name="checkout"),
    path("updateitem/",views.update_item, name="updateitem"),
    path("proces_orden/",views.procesarOrden, name="proces_orden"),
]