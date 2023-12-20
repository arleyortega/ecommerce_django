import json
from . models import *

def cookieCart(request):
    try:
        carro = json.loads(request.COOKIES['carro'])
    except json.JSONDecodeError as   e :
        print(f"Error decoding JSON: {e}")
        carro = {}

        
    print('carro:', carro)
    items=[]
    orden= {'get_cart_total':0  , 'get_cart_items':0,'shipping': False}
    cartItems = orden['get_cart_items']
    for i in carro:
        try:
            cartItems += carro[i]["cantidad"]
            producto = Product.objects.get(id=i)
            total = (producto.precio* carro[i]["cantidad"])
            orden['get_cart_total'] += total 
            orden['get_cart_items'] += carro[i]['cantidad']
            
        
            item = {
				'id':producto.id,
				'producto':{'id':producto.id,'nombre':producto.nombre, 'precio':producto.precio, 
				'imageURL':producto.imageURL}, 'cantidad':carro[i]['cantidad'],
				'digital':producto.digital,'get_total':total,
				}
           
            items.append(item)
            if producto.digital == False:
                orden['shipping'] = True
        except:
            pass
    return {'cartItems':cartItems,'orden':orden,'items':items}

				
def cartData(request):
    if request.user.is_authenticated:
        cliente = request.user.client
        orden ,created = Orden.objects.get_or_create(cliente=cliente, complete=False)
        items = orden.orderitem_set.all()
        cartItems = orden.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        orden = cookieData['orden']
        items = cookieData['items']
            
    return {'cartItems': cartItems,'orden': orden, 'items': items}

def guestOrden(request, data):
    print('El usuario no esta registrado')
    print('COOKIES',request.COOKIES)
    nombre = data['form']['nombre']
    email =data['form']['email']
    cookieData = cookieCart(request)
    items = cookieData['items']
    cliente , created = client.objects.get_or_create(
        email=email,
        )
    cliente.nombre = nombre
    cliente.save()

    orden= Orden.objects.create(
        cliente = cliente,
        complete = False
        )
    for item in items:
        producto = producto.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            producto = producto,
            orden = orden,
            cantidad = item['cantidad']
            )   
    return cliente, orden