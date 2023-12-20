from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class client(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True , blank=True)
    nombre = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200 , null=True)
    def __str__(self):
        return self.nombre

class Product(models.Model):
    nombre = models.CharField(max_length=200 , null=True)
    precio = models.DecimalField(max_digits=7,decimal_places=2)
    digital = models.BooleanField(default=False , null=True, blank=False)
    imagen = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.nombre
    @property
    def imagen_url(self):
        try: url =self.imagen.url
        except:
            url = ''
        return url

class Orden(models.Model):
    cliente = models.ForeignKey(client, on_delete=models.SET_NULL, blank=True , null=True)
    fecha_orden = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True , blank=False)
    id_transaccion = models.CharField(max_length=200, null=True)
    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.producto.digital == False:
                shipping = True
        return shipping 
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum(item.get_total for item in orderitems)
        return total
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum(item.cantidad for item in orderitems)
        return total
    

class OrderItem(models.Model):
    producto = models.ForeignKey(Product, on_delete=models.SET_NULL , blank=True , null=True)
    orden = models.ForeignKey(Orden, on_delete=models.SET_NULL, blank=True , null=True)
    cantidad = models.IntegerField(default=0, null=True , blank=True)
    fecha_add = models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        total = self.producto.precio * self.cantidad
        return total

class DireccionCompra(models.Model):
    cliente = models.ForeignKey(client, on_delete=models.SET_NULL, blank=True , null = True)
    orden = models.ForeignKey(Orden, on_delete=models.SET_NULL , blank=True , null = True)
    direccion = models.CharField(max_length=200 , null=True)
    ciudad = models.CharField(max_length=200 , null=True)
    departamento = models.CharField(max_length=200 , null=True)
    codigo_postal = models.CharField(max_length=200 , null=True)
    fecha_add=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.direccion
    