divVacantRoom = document.getElementById('div_vacant_room')
if(divVacantRoom) {
    const value = divVacantRoom.dataset.vacantRoom;
    const div_a = document.getElementById('pointerEvent');
    const errorText = document.getElementById('errorVacantRoom')

    if (value == 0) {
        errorText.style.display = 'block';
        if(div_a) {
            div_a.style.pointerEvents = "none";
            div_a.querySelector('a').classList.remove('text-primary');
            div_a.querySelector('a').classList.remove('border-secondary');
            div_a.querySelector('a').classList.add('border-dark');
        }
    } else {
        errorText.style.display = 'none';
        if(div_a) {
            div_a.style.pointerEvents = 'auto';
            div_a.querySelector('a').classList.add('text-primary');
            div_a.querySelector('a').classList.remove('border-dark');
            div_a.querySelector('a').classList.add('border-secondary');
        }
    }
}

input_search_room = document.getElementById("input-search-room")
if(input_search_room) {
    document.getElementById('a-search-room').href = window.location.href.split('&').slice(0,1).join('');
    input_search_room.addEventListener('input', function() {
        if(document.getElementById('a-search-room').href.includes('?')) {
            if(document.getElementById('a-search-room').href.includes('key_search=')) {
                document.getElementById('a-search-room').href = document.getElementById('a-search-room').href.split('=').slice(0,1).join('') + "=" + this.value;
            }
            else {
                document.getElementById('a-search-room').href = document.getElementById('a-search-room').href + "&key_search=" + this.value;
            }
        }
        else {
            document.getElementById('a-search-room').href = document.getElementById('a-search-room').href + "?key_search=" + this.value;
        }
    });
}

function formatCurrency(value) {
    var amountInVND = value * 1000;
    return amountInVND.toLocaleString('vi-VN');
}

prices = document.querySelectorAll('.price')
if(prices) {
    for(let i = 0; i < prices.length; i++) {
        prices[i].textContent = "Price: " + formatCurrency(prices[i].textContent) + " VND"
    }
}