const customModal = document.getElementById('customModal');
const showCustomModalButtons = document.querySelectorAll('.showCustomModal');
const closeCustomModal = document.getElementById('closeCustomModal');
const closeCustomModalIcon = document.getElementById('closeCustomModalIcon');

showCustomModalButtons.forEach(button => {
    button.addEventListener('click', function () {
        customModal.style.display = 'flex';
    });
});

closeCustomModal.addEventListener('click', function () {
    customModal.style.display = 'none';
});

closeCustomModalIcon.addEventListener('click', function () {
    customModal.style.display = 'none';
});

window.addEventListener('click', function (event) {
    if (event.target === customModal) {
        customModal.style.display = 'none';
    }
});