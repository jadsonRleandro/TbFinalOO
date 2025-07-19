function validation() {
    let user = document.getElementById('username');
    let password = document.getElementById('password');
    let confPassword = document.getElementById('checkpassword');

    let verification = 0;

    if (user.value =='' || password.value == '' || confPassword.value == '') {
        alert('Preencha todos os campos.');
        verification = 1;
    } else {
        if (password.value != confPassword.value) {
            alert('As senhas estão diferentes.');
            verification = 1;
        }

        if (password.value.length < 7) {
            alert('A senha deve ter no mínimo 7 caracteres.');
            verification = 1;
        }

        if (user.value.length < 4) {
            alert("O usuário deve ter no mínimo 4 caracteres.");
            verification = 1;
        }
    }

    if (verification == 0) {
        let form = document.getElementById('container')
        form.submit()
    }
    
}