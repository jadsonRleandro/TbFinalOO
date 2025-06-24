document.body.style.overflow = "hidden"
let usuario = document.getElementById("username")
const load = document.getElementById("load")
load.addEventListener("animationend", (event) => {
    load.innerHTML = ""
    load.style = "    width: 0px; height: 0px;"
    document.body.style.overflow = "auto"
})

let actMusic = ''

const actBtn = document.getElementById('actBtn')
const pauseIcon = "/static/img/pauseIcon.png"
const playIcon = "/static/img/playIcon.png"

function play(self) {
    child = self.children[0]

    if (actMusic != '' && actMusic != child){
        actMusic.src = playIcon
        actMusic.className = 'playIcon' 
    }

    actMusic = child

    if (child.classList[0] == 'pauseIcon') {
        child.src = playIcon
        child.className = 'playIcon'
        actBtn.src = playIcon
        actBtn.className = 'playIcon'
    }
    else {
        child.src = pauseIcon
        child.className = 'pauseIcon'
        actBtn.src = pauseIcon
        actBtn.className = 'pauseIcon'
    }
}

let menuGui = 0

function openMenu(){
    const menu = document.getElementById('menu')
    if (menuGui == 0){
        menuGui = 1
        menu.style = "height: 100vh; width: 40%;"
        menu.innerHTML = `        
        <div id="userInfos">
            <input onclick="openMenu()" type="button" id="avatar" src="">
            <h1 id="username">usuario</h1>
        </div>
        <br>
        <br>
        <br>
        <div class="menuOption">Adicionar Musica</div>
        <div class="menuOption">Remover Musica</div>
        <div class="menuOption">Conta</div>

        <h2 id="logout">LOGOUT<img src="./static/img/exitIcon.png"></h2>`
    }else{
        menuGui = 0
        menu.innerHTML = ''
        menu.style = "height: 0px; width:0px"
    }
}