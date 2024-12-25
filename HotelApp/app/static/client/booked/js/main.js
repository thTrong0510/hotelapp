tableBook = document.getElementById('tableBooked')
if(tableBook) {
    rows = tableBook.querySelectorAll('tr')
    bookedBtns = document.querySelectorAll('.bookedBtn')
    for(let i = 1; i < rows.length; i++) {
        const status = rows[i].querySelectorAll('td')[0].querySelector('button').dataset.status;
        if (status === "False") {
            bookedBtns[i - 1].type = 'button'; // Disable button nếu vacant_room = 0
            bookedBtns[i - 1].title = 'Book overdue'; // Thêm title cho hover để thông báo lỗi
            bookedBtns[i - 1].classList.remove('text-primary');
            bookedBtns[i - 1].classList.remove('border-secondary');
            bookedBtns[i - 1].classList.add('border-dark');
            bookedBtns[i - 1].style.pointerEvents = "none"
        }
    }

     for(let i = 1; i < rows.length; i++) {
        var checkInDate = rows[i].querySelectorAll('td')[5].querySelector('p').textContent;
        var checkOutDate = rows[i].querySelectorAll('td')[6].querySelector('p').textContent;

        if( rows[i].querySelectorAll('td')[4].querySelector('p.accurate_')) {
            var accurateDate = rows[i].querySelectorAll('td')[4].querySelector('p.accurate_').textContent;
            rows[i].querySelectorAll('td')[4].querySelector('p.accurate_').textContent = accurateDate.split(' ').slice(0, 1).join('');
        }
        rows[i].querySelectorAll('td')[5].querySelector('p').textContent = checkInDate.replace('00:00:00', '');
        rows[i].querySelectorAll('td')[6].querySelector('p').textContent = checkOutDate.replace('00:00:00', '');
    }

    priceBookeds = document.querySelectorAll('.priceBooked')
    for(let i = 0; i < priceBookeds.length; i++) {
        priceBookeds[i].textContent = (priceBookeds[i].textContent * 1000).toLocaleString('vi-VN');
    }

}
