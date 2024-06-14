$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 1,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$(".plus-cart").click(function(){
    let id = $(this).attr("pid").toString();
    let element = this.parentNode.children[2]
    $.ajax({
        type:"GET",
        url:"/plus-cart",
        data: {
            prod_id:id
            },
        success:function(data){
            element.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalAmount").innerText = data.totalAmount
            }
        })
})

$(".minus-cart").click(function(){
    let id = $(this).attr("pid").toString();
    let element = this.parentNode.children[2]
    $.ajax({
        type:"GET",
        url:"/minus-cart",
        data: {
            prod_id:id
            },
        success:function(data){
            element.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalAmount").innerText = data.totalAmount    
        }
        })
})

$(".remove-cart").click(function(){
    let id = $(this).attr("pid").toString();
    element = this
    $.ajax({
        type: "GET",
        url: "/remove-cart",
        data: {
            prod_id:id
        },
        success: function(data){
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalAmount").innerText = data.totalAmount   
            element.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})