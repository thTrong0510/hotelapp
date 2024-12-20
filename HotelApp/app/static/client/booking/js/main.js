formSudmit = document.getElementById('bookingForm');
if(formSudmit) {
    formSudmit.addEventListener('submit', function(event) {
        event.preventDefault();
        // Ngăn form submit mặc định
        const phoneInput = document.getElementById('customer_phone');
        const phoneValue = phoneInput.value.trim();
        const phoneErrorElement = document.getElementById('phoneError');
        const phoneRegex = /^(?:\+84|0)(?:[3|5|7|8|9][0-9]{8}|(?:1[1|6|8|9]|2[1-9]|4[2-9])[0-9]{7})$/;

        const checkInError = document.getElementById('checkInError');
        const checkOutError = document.getElementById('checkOutError');
        const checkInInput = document.getElementById('checkIn');
        const checkOutInput = document.getElementById('checkOut');

        const checkInDate = new Date(checkInInput.value);
        const checkOutDate = new Date(checkOutInput.value);
        const today = new Date();

        // Loại bỏ giờ phút, chỉ lấy ngày
        checkInDate.setHours(0, 0, 0, 0);
        checkOutDate.setHours(0, 0, 0, 0);
        today.setHours(0, 0, 0, 0);

        // Clear previous errors
        if (checkInInput.classList.contains('error')) {
            checkInInput.classList.remove('error');
        }
        if (checkOutInput.classList.contains('error')) {
            checkOutInput.classList.remove('error');
        }
        if (phoneInput.classList.contains('error')) {
            phoneInput.classList.remove('error');
        }

        phoneErrorElement.textContent = '';
        checkInError.textContent = '';
        checkOutError.textContent = '';

        if (!phoneRegex.test(phoneValue)) {
            phoneInput.classList.add('error');  // Thêm lớp error vào input
            phoneErrorElement.textContent = 'Invalid phone number.';  // Hiển thị thông báo lỗi
        }

        // Check-in date must not be before today
        if (checkInDate < today) {
            checkInInput.classList.add('error');
            checkInError.textContent = 'Check-in date cannot be before today.';
        }

        // Check-out date must not be before today
        if (checkOutDate < today) {
            checkOutInput.classList.add('error');
            checkOutError.textContent = 'Check-out date cannot be before today.';
        }

        if (checkOutDate < checkInDate) {
            checkOutInput.classList.add('error');
            checkOutError.textContent = 'Check-out date cannot be before check-in date';
        }

        // Check-out date must be within 28 days after check-in
        const maxCheckOutDate = new Date(checkInDate);
        maxCheckOutDate.setDate(checkInDate.getDate() + 28);

        if (checkOutDate > maxCheckOutDate) {
            checkOutInput.classList.add('error');
            checkOutError.textContent = 'Check-out date must not be more than 28 days after check-in.';
        }

        if (checkInInput.classList.contains('error') || checkOutInput.classList.contains('error') || phoneInput.classList.contains('error')) {
            return;
        }
        this.submit();
    });
}

// Lấy các phần tử
const priceInput = document.getElementById('price_booking');
const quantityInput = document.getElementById('quantity_booking');
const numGuestInput = document.getElementById('numGuests_booking');
const basePrice = parseFloat(priceInput.dataset.basePrice) || 0;
const roomCountMultiplier = parseFloat(priceInput.dataset.roomCountMultiplier) || 0;
const sessionMultiplier = parseFloat(priceInput.dataset.sessionMultiplier) || 0;
const dailyMultiplier = parseFloat(priceInput.dataset.dailyMultiplier) || 0;
const foreignGuestMultiplier = parseFloat(priceInput.dataset.foreign_guest_multiplier) || 0;

// Hàm tính giá
function calculatePrice() {
    const quantity = parseFloat(quantityInput.value) || 0;
    const numGuest = parseFloat(numGuestInput.value) || 0;

    var totalPrice = basePrice * dailyMultiplier * dailyMultiplier;
    if(quantity > 1) {
        var price = totalPrice;
        for(let i = 1; i < quantity; i++) {
            totalPrice = totalPrice + price * roomCountMultiplier;
        }
    }

    // Gán giá trị mới vào trường price
    priceInput.value = totalPrice.toFixed(2); // Giới hạn 2 chữ số thập phân
}

// Gắn sự kiện input để tính lại giá khi quantity hoặc factor thay đổi
if(quantityInput) {
    quantityInput.addEventListener('change', calculatePrice);
}
if(numGuestInput) {
    numGuestInput.addEventListener('change', calculatePrice);
}

// Tính giá ban đầu
calculatePrice();
