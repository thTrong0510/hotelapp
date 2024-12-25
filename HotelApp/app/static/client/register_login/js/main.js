div_check_login = document.getElementById('check_login')
if(div_check_login) {
    inputs = document.querySelectorAll('.form-control')
    for(let i = 0; i < inputs.length; i++) {
        inputs[i].addEventListener('focus', function() {
            div_check_login.style.display = "none";
        });
    }
    check_account = document.getElementById('checkAccount')
    if(check_account.dataset.checkAccount === "False") {
        div_check_login.textContent = "Something is wrong, Please Double-check!";
        div_check_login.style.display = "block";
    }
    if(check_account.dataset.statusAccount === "False") {
        div_check_login.textContent = "The account has been locked!";
        div_check_login.style.display = "block";
    }
}