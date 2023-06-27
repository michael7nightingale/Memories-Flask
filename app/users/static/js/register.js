function flushMessage(element, msg){

}


function validateEmail(event){
    let emailInput = document.getElementById("email");
    let email = emailInput.value;
    if (!(email.length > 5 && "@" in email)){
        window.alert("Email is not correct");
        return false;
    }
    return true;

}

function validatePassword() {
        let password = document.getElementById("txtPassword").value;
        let confirmPassword = document.getElementById("txtConfirmPassword").value;
        if (password !== confirmPassword) {
            alert("Passwords do not match.");
            return false;
        }
        return true;
    }

function validateForm(event){
    console.log(123);
    validateEmail();
    validatePassword();

}
