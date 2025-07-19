const password = document.getElementById('password');
const botao = document.getElementById('botao-toggle')

const senhaReal = password.textContent.trim();

let mostrando = false;

function showHide() {
    if (mostrando) {
    password.textContent = "*********";
    botao.src = "/static/assets/hide.png";
    mostrando =false
    } else {
    password.textContent = senhaReal;
    botao.src = "/static/assets/show.png";
    mostrando = true
  }
}

function returnMenu(){
    const form = document.getElementById('retornarMenu')
    form.submit()
}
function validation() {
    if (confirm("Tem certeza que deseja deletar sua conta? Essa ação é irreversível.")) {
        document.getElementById('conta-delete').submit();
    }
}