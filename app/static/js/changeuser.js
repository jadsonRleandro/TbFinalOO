
function trocaruser(event) {
    event.preventDefault();

    if (confirm("Tem certeza que deseja trocar o username? Essa ação é irreversível.")) {
        let form = document.getElementById('trocar-user');
        form.submit();
    }
}

function changeFoto(element) {
    const src = element.getAttribute('src');
    if (confirm("Tem certeza que deseja trocar a foto de perfil?")) {
        let form = document.getElementById('change-photo');
        form.querySelector('#photoInput').value = src;
        form.submit();
    }
}