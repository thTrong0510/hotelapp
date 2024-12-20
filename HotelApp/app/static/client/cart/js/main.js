table = document.getElementById('tableCart')
if(table) {
    rows = table.querySelectorAll('tr')
    cartBtns = document.querySelectorAll('.cartBtn')
    for(let i = 1; i < rows.length; i++) {
        const vacantRoom = rows[i].querySelectorAll('td')[4].querySelector('p').dataset.vacantRoom;
        if (vacantRoom == 0) {
            cartBtns[i - 1].type = 'button'; // Disable button nếu vacant_room = 0
            cartBtns[i - 1].title = 'No vacant rooms available'; // Thêm title cho hover để thông báo lỗi
            cartBtns[i - 1].classList.remove('text-primary');
            cartBtns[i - 1].classList.remove('border-secondary');
            cartBtns[i - 1].classList.add('border-dark');
            cartBtns[i - 1].style.pointerEvents = "none"
        }
    }
}
