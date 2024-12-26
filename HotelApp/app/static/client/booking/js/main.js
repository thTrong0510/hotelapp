formSudmit = document.getElementById('bookingForm');
const checkInInput = document.getElementById('checkIn');
const checkOutInput = document.getElementById('checkOut');
if(document.getElementById('price_booking')) {
    document.getElementById('price_booking').value = (document.getElementById('price_booking').value * 1000).toLocaleString('vi-VN');
}
if(formSudmit) {
    formSudmit.addEventListener('submit', function(event) {
        event.preventDefault();
        // Ngăn form submit mặc định
        const CCCDInput = document.getElementById('customer_cccd');
        const CCCDValue = CCCDInput.value.trim();
        const CCCDErrorElement = document.getElementById('cccdError');
        const CCCDRegex = /^0\d{11}$/;

        const checkInError = document.getElementById('checkInError');
        const checkOutError = document.getElementById('checkOutError');

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
        if (CCCDInput.classList.contains('error')) {
            CCCDInput.classList.remove('error');
        }

        CCCDErrorElement.textContent = '';
        checkInError.textContent = '';
        checkOutError.textContent = '';

        if (!CCCDRegex.test(CCCDValue)) {
            CCCDInput.classList.add('error');  // Thêm lớp error vào input
            CCCDErrorElement.textContent = 'Invalid CCCD number.';  // Hiển thị thông báo lỗi
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
        revPeriodCheckin = parseFloat(document.getElementById('price_booking').dataset.reversePeriodCheckin) || 0;
        const maxCheckOutDate = new Date(checkInDate);
        maxCheckOutDate.setDate(checkInDate.getDate() + revPeriodCheckin);

        if (checkOutDate > maxCheckOutDate) {
            checkOutInput.classList.add('error');
            checkOutError.textContent = 'Check-out date must not be more than ' + revPeriodCheckin + ' days after check-in.';
        }

        if (checkInInput.classList.contains('error') || checkOutInput.classList.contains('error') || CCCDInput.classList.contains('error')) {
            return;
        }

        this.submit();
    });
}

// Lấy các phần tử
const priceInput = document.getElementById('price_booking');
const quantityInput = document.getElementById('quantity_booking');
const numGuestInput = document.getElementById('numGuests_booking');
const numberOfForeignersInput = document.getElementById('number_foreigners');

// Hàm tính giáreverse-period-checkin
function calculatePrice() {
    const basePrice = parseFloat(priceInput.dataset.basePrice) || 0;
    const roomCountMultiplier = parseFloat(priceInput.dataset.roomCountMultiplier) || 0;
    const sessionMultiplier = parseFloat(priceInput.dataset.sessionMultiplier) || 0;
    const dailyMultiplier = parseFloat(priceInput.dataset.dailyMultiplier) || 0;
    const foreignMultiplier = parseFloat(priceInput.dataset.foreignGuestMultiplier) || 0;
    const quantity = parseFloat(quantityInput.value) || 0;
    const numberOfForeigners = parseFloat(numberOfForeignersInput.value) || 0;
    var totalPrice = basePrice * dailyMultiplier;
    var dates = calculateDaysDifference();
    if(quantity > 1) {
        var price = totalPrice;
        for(let i = 1; i < quantity; i++) {
            totalPrice = totalPrice + price * roomCountMultiplier;
        }
    }
    if(numberOfForeigners > 0) {
        totalPrice = totalPrice + totalPrice * foreignMultiplier;
    }
    if(dates > 0) {
        totalPrice = totalPrice * (dates + 1);
    }

    totalPrice = totalPrice * 1000;

    // Gán giá trị mới vào trường price
    priceInput.value = totalPrice.toLocaleString('vi-VN'); // Giới hạn 2 chữ số thập phân
}

// Gắn sự kiện input để tính lại giá khi quantity hoặc factor thay đổi
if(quantityInput) {
    quantityInput.addEventListener('change', calculatePrice);
}
if(numberOfForeignersInput) {
    numberOfForeignersInput.addEventListener('change', calculatePrice);
}

const totalGuestsInput = document.getElementById("numGuests_booking");

// Hàm kiểm tra và giới hạn giá trị của NumberOfForeigners
function validateNumberOfForeigners() {
    const totalGuests = parseInt(totalGuestsInput.value) || 0;
    const numberOfForeigners = parseInt(numberOfForeignersInput.value) || 0;

    // Nếu số người nước ngoài vượt quá tổng số khách, đặt lại giá trị
    if (numberOfForeigners > totalGuests) {
        numberOfForeignersInput.value = totalGuests;
    }
}

// Gắn sự kiện lắng nghe thay đổi giá trị
if(numberOfForeignersInput) {
    numberOfForeignersInput.addEventListener("input", validateNumberOfForeigners);
}
if(totalGuestsInput) {
    totalGuestsInput.addEventListener("input", validateNumberOfForeigners);
}

function calculateDaysDifference() {
    // Kiểm tra nếu cả hai ngày đều hợp lệ
    const checkIn = new Date(checkInInput.value);
    const checkOut = new Date(checkOutInput.value);
    if (!isNaN(checkIn) && !isNaN(checkOut)) {
        const differenceInTime = checkOut - checkIn; // Khoảng cách thời gian tính bằng milliseconds
        const differenceInDays = differenceInTime / (1000 * 60 * 60 * 24); // Đổi từ milliseconds sang ngày
        return Math.max(differenceInDays, 0); // Đảm bảo không trả về giá trị âm
    }
}

if(checkInInput) {
    checkInInput.addEventListener("change", calculatePrice);
}
if(checkOutInput){
    checkOutInput.addEventListener("change", calculatePrice);
}
