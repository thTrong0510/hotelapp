function count_product(name, description, short_desc, price, capacity, quantity, vacant_room, active, room_type_id) {
    alert("hello");
    fetch('/api/carts', {
        method: 'post',
        body: JSON.stringify({
            "name": name,
            "description": description,
            "short_desc": short_desc,
            "price": price,
            "capacity": capacity,
            "quantity": quantity,
            "vacant_room": vacant_room,
            "active": active,
            "room_type_id": room_type_id
        }),
        headers: {
        'Content-Type':'application/json'
        }
    }).then(res => res.json()).then(data => {
    let items = document.getElementsByClassName("counter");
    for(let item of items)
        item.innerText = data.total_quantity
    })
}