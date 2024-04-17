function changeLocationCart() {
    window.location.href = '/cart'
}
function changeLocationLogin() {
    window.location.href = '/login'
}
function changeLocationOrder() {
    window.location.href = '/order'
}
function changeLocationCollection() {
    window.location.href = '/collection'
}
const categories = document.getElementById('catalog__categories')
const products = document.getElementById('catalog__content')
let counter = {}
main()
async function main(){
    await get_categories()
    await update_all_products()
}
async function get_categories() {
    let response = await fetch(
        "http://192.168.3.11:1000/get-categories", {
            method: 'GET'
        });
    if (response.ok) {
        let data = await response.json()
        console.log(data)
        let li = document.createElement('li')
        li.id = 'all'
        li.addEventListener('click', change_category)
        li.innerText = 'Все'
        categories.appendChild(li)
        for (let i = 0; i < data.length; i++) {
            let li = document.createElement('li')
            li.id = data[i]
            li.addEventListener('click', change_category)
            li.innerText = data[i]
            categories.appendChild(li)
        }
    } else {
        console.log('error')
    }
}
async function update_all_products() {
    let response = await fetch(
        `http://192.168.3.11:1000/catalog`, {
            method: "GET"
        }
        )
    if (response.ok) {
        data = await response.json()
        await update_products(data)
    }
}
async function change_category(event) {
    if (event.type === 'click') {
        let response;
        if (event.target.id === 'all') {
            response = await fetch(`http://192.168.3.11:1000/catalog`, {
                method: "GET"
            })
        }
        else{
            response = await fetch(`http://192.168.3.11:1000/catalog?category=${event.target.id}`, {
                method: "GET"
            })
        }
        if (response.ok) {
            data = await response.json()
            console.log(data);
            event.className = 'catalog__item'
            event.target.className = 'catalog__item active'
            await update_products(data)
        } else {
            console.log('error')
        }
    }
}
async function update_products(data) {
    products.innerHTML = ''
    for (const [key, value] of Object.entries(data)) {
        let div = document.createElement('div')
        div.id = key
        div.className = 'catalog__card'
        let image = document.createElement('img')
        image.src = `static/${value.images[0]}`
        image.style.width = 400
        image.style.length = 600
        div.appendChild(image)
        let div_name = document.createElement('div')
        let div_description = document.createElement('div')
        let div_price = document.createElement('div')
        let div_quantity = document.createElement('div')
        div_name.className = 'catalog__card-name'
        div_description.className = 'catalog__card-description'
        div_price.className = 'catalog__card-price'
        div_quantity.className = 'catalog__card-quantity'
        div_name.innerHTML = value.name
        div_description.innerHTML = value.description
        div_price.innerHTML = value.price + '₽'
        div_quantity.innerHTML = 'В наличии - ' + value.quantity
        div.append(div_name, div_description, div_price, div_quantity)
        let button = document.createElement('button')
        button.type = 'button'; button.id = key; button.addEventListener("click", add_to_cart); button.innerText='Добавить в корзину'
        div.appendChild(button)
        //if (value.images[0] != null) {
        //
        //    for (let i = 0; i < value.images.length; i++) {
        //    let image = document.createElement('img')
        //    let button = document.createElement('button')
        //    button.type = 'button'
        //    button.id = key
        //    button.addEventListener("click", add_to_cart)
        //    console.log(value.images[i])
        //    image.src = `static/${value.images[i]}`
        //    image.style.width = 400
        //    image.style.length = 600
        //    div.appendChild(image)
        //    }
        //}
        products.appendChild(div)
    }
}
async function add_to_cart(event) {
    let myHeaders = new Headers();
    myHeaders.set('Authorization', localStorage.getItem('access_token'));
    console.log(localStorage.getItem('access_token'))
    console.log(myHeaders)
    response = await fetch(
        `http://192.168.3.11:1002/add-to-cart`, {
            method: "PUT",
            body: JSON.stringify({product_id: Number(event.target.id)}),
            headers: {'Authorization': localStorage.getItem('access_token'), 'Accept': 'application/json', 'Content-Type': 'application/json'},
        })
    if (response.ok) {
        if (event.target.id in counter){
            counter[event.target.id] = counter[event.target.id] + 1
        }
        else {
            counter[event.target.id] = 1
        }
        event.target.innerText = `Добавить в корзину - ${counter[event.target.id]}`
    } else {
        if (response.status === 401){
            alert('Вам нужно авторизоваться')
        }
        else{
            alert('Товар закончился')
        }
    }
}