from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(client)
admin.site.register(Product)
admin.site.register(Orden)
admin.site.register(OrderItem)
admin.site.register(DireccionCompra)
