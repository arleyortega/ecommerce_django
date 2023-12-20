var update_btn = document.getElementsByClassName('update-cart')

for  ( var i = 0; i < update_btn.length; i++){
    update_btn[i].addEventListener('click', function(){
        var productID = this.dataset.producto
        var action = this.dataset.action
        console.log('productID:',productID, 'action:',action)
        console.log('USER:', user)
        if (user =='AnonymousUser'){
            console.log('user is not authenticated')
        }else{
            console.log('User is authenticated , sending data...')
        }
       
        
    })
}

function addCookieItem(productID, action){
    console.log('usuario no esta autenticado')
    if (action=='add'){
        if(carro[productID] == undefined){
            carro[productID] == {'cantidad': 1}

        }else{
            carro[productID]['cantidad'] += 1
        }
    }
    if(action == 'remove'){
        carro[productID]['cantidad'] -= 1
    }
    if(carro[productID]['cantidad'] <= 0){
        console.log('borar item')
        delete carro[productID]
    }
    console.log('cart:',carro)
    document.cookie = 'cart=' + JSON.stringify(carro) + ";domain=;path/"
    location.reload()

}



function updateUserOrden(productID, action){
    
    console.log('user is loged in , sending data...')
    var url ='/updateitem/'
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productID':productID, 'action':action})
    .then((Response) =>{
            return  Response.json();

        })
    .then((data) =>{
            console.log('data:',data)
        })
    });
}
