//creating event handler for each button
var updateBtns = document.getElementsByClassName('update-cart') 
//we querry all the cart item by the class update-cart

for(var i = 0; i<updateBtns.length; i++){
    //looping through all the buttons
    updateBtns[i].addEventListener('click',function(){
        //adding event listener on click 
        var productId = this.dataset.product
        //get product id we set
        var action = this.dataset.action
        //get action
        console.log('productId:',productId,'Action:',action)

        console.log('USER',user)
        if (user == 'AnonymousUser'){
            console.log('User is not auhenticated')
        }else{
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId,action){
    //create a function in our event handler
    console.log("user authenticated, sending data")

    var url='/update_item/' //url to send post data to 

    //for fetch call, we make a post request and were gonna send the data to the new view updateItem. we send productId and action to  the backend updateItem to which will process it
    fetch(url, {
        method:'POST',  //what kind of data we will send to the backend(type=post)
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken' : csrftoken,
        },
        body:JSON.stringify({'productId':productId,'action':action})  //body is the data that we send to the backend
    })

    .then((response) =>{         //to receive a response after updateItem does some processing on data
        return response.json()
    })

    .then((data) =>{
        console.log('data:',data)
        //what view is sending back to our template
        location.reload() //to relaod our page
    })
}