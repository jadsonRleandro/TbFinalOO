function login() {
    let user = document.getElementById('username');
    let password = document.getElementById('password');

    let verification = 0;

    if (user.value === '' || password.value === '') {
        alert('Preencha todos os campos.');
        verification = 1;
    }
    console.log(verification)

    if (verification === 0) {
        let form = document.getElementById('container')
        form.submit()
    }
}