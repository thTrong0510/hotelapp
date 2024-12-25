table = document.getElementById('customerTable')
if(table) {
    rows = table.querySelectorAll('tr')
    for(let i = 1; i < rows.length; i++) {
        rows[i].querySelectorAll('td')[1].textContent = rows[i].querySelectorAll('td')[1].textContent.split('.').slice(1, 2).join('');
    }
}

ul = document.getElementById('ulDetail');
if(ul) {
    li = ul.querySelectorAll('li');
    li[3].textContent = "User Type: " + li[3].textContent.split('.').slice(1, 2).join('');
}

tableBooked = document.getElementById('tableBookedStaff')
if(tableBooked) {
    rows = tableBooked.querySelectorAll('tr')
    for(let i = 1; i < rows.length; i++) {
        var checkInDate = rows[i].querySelectorAll('td')[5].querySelector('p').textContent;
        var checkOutDate = rows[i].querySelectorAll('td')[6].querySelector('p').textContent;

        rows[i].querySelectorAll('td')[5].querySelector('p').textContent = checkInDate.replace('00:00:00', '');
        rows[i].querySelectorAll('td')[6].querySelector('p').textContent = checkOutDate.replace('00:00:00', '');
    }
}


//
const modal = document.getElementById('staffModal');
const openModalBtn = document.querySelectorAll('.openStaffModal');
const closeModalBtn = document.querySelector('.staff-close-btn');
const yesBtn = document.getElementById('yesBtn');
const noBtn = document.getElementById('noBtn');

if(document.querySelectorAll('.staff-customer-id')) {
    document.querySelectorAll('.staff-customer-id').forEach(blockBtn => {
        blockBtn.addEventListener('click', (e) => {
            customer_id = blockBtn.dataset.customerId;
            yesBtn.value = JSON.stringify({ customer_id: customer_id });
        });
    });
}

if(modal){
    // Hiển thị modal khi nhấn nút
    for(let i =0; i < openModalBtn.length; i++) {
        openModalBtn[i].addEventListener('click', () => {
            modal.style.display = 'flex';
        });
    }

    // Đóng modal khi nhấn nút "x"
    closeModalBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Đóng modal khi nhấn ra ngoài modal
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Xử lý sự kiện nút Yes
    yesBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Xử lý sự kiện nút No
    noBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
}

const staffCustomerIds = document.querySelectorAll('.staff-customer-id')
if(staffCustomerIds) {
    for(let i = 0; i < staffCustomerIds.length; i++) {
        if(staffCustomerIds[i].dataset.customerStatus  === "False") {
            staffCustomerIds[i].querySelector('a').textContent = "Unblock";
        }
        else {
            staffCustomerIds[i].querySelector('a').textContent = "Block";
        }
    }
}

