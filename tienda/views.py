from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from . utils import cookieCart,guestOrden,cartData

# Create your views here.
def index(request):
    data = cartData(request)
    cartItems = data['cartItems']
    productos = Product.objects.all()
    contexto={'productos':productos, 'cartItems': cartItems}
    return render(request,"tienda/index.html",contexto)

def carro(request):
    data = cartData(request)
    cartItems = data['cartItems']
    orden = data['orden']
    items = data['items']

            
            

    contexto={'items':items , 'orden':orden, 'cartItems': cartItems}
    return render(request, "tienda/carro.html",contexto)



def checkout(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    orden = data['orden']
    items = data['items']
            
    contexto={'items':items , 'orden':orden, 'cartItems': cartItems}
    return render(request, "tienda/checkout.html", contexto)


def update_item(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    print('Action: ', action)
    print('ProductID: ', productID)

    cliente = request.user.client
    producto = Product.objects.get(id=productID) 
    orden, created = Orden.objects.get_or_create(cliente = cliente , complete=False)
    orderItem, created = OrderItem.objects.get_or_create(orden =orden,producto = producto)

    if action == 'add':
        orderItem.cantidad = (orderItem.cantidad + 1)
    elif action == 'remove':
        orderItem.cantidad = (orderItem.cantidad - 1)
    orderItem.save()
    
    if orderItem.cantidad <= 0:
        orderItem.delete()
    response_data = {'message': 'El item fue añadido'}
    return JsonResponse(response_data)


def procesarOrden(request):
    print('Datos:',request.body)
    id_transaccion = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        cliente = request.user.client
        orden_instance, created = Orden.objects.get_or_create(cliente = cliente , complete = False)
    
        
    else:
       cliente, orden = guestOrden(request, data)
    total =float(data['form']['total'])
    orden_instance.id_transaccion = id_transaccion
    if total == orden_instance.get_cart_total:
        orden_instance.complete = True
    orden_instance.save()

    if orden_instance.shipping == True:
            DireccionCompra.objects.create(
                cliente = cliente,
                orden = orden_instance,
                direccion = data['shipping']['direccion'],
                ciudad = data['shipping']['ciudad'],
                departamento = data['shipping']['departamento'],
                codigo_postal = data['shipping']['codigoPostal'],
            )
    return JsonResponse({'message':'pago completado'})
    
   