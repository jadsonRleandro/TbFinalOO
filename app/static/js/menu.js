// load inicial

document.body.style.overflow = "hidden"

const load = document.getElementById("load")
load.addEventListener("animationend", (event) => {
    load.innerHTML = ""
    load.style = "    width: 0px; height: 0px;"
    document.body.style.overflow = "auto"
})

// funçao quando clica no play

let actMusic = ''

const actBtn = document.getElementById('actBtn')
const pauseIcon = "/static/assets/pauseIcon.png"
const playIcon = "/static/assets/playIcon.png"

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

// abrindo e fechando o menu

let menuGui = 0

function openMenu(){
    const menu = document.getElementById('menu')
    if (menuGui == 0){
        menuGui = 1
        menu.style = "height: 100vh; width: 40%;"
        menu.innerHTML = `        
        <div id="userInfos">
            <input onclick="openMenu()" type="button" id="avatar" src="">
            <h1 id="username">Usuario</h1>
        </div>
        <br>
        <br>
        <br>
        <div class="menuOption">Adicionar Musica</div>
        <form onclick = "submitForm(this)" action = "/remove" method = "get" class="menuOption">Remover Musica</form>
        <div class="menuOption">Conta</div>

        <h2 id="logout">LOGOUT<img src="./static/assets/exitIcon.png"></h2>`
    }else{
        menuGui = 0
        menu.innerHTML = ''
        menu.style = "height: 0px; width:0px"
    }
}


// PEGANDO AS MUSICAS PELO URL

window.onload = getMusic()

function getMusic(){
    pbMusic = []
    pvMusic = []
    const publicMusics = document.getElementsByClassName('public')
    const privateMusics = document.getElementsByClassName('private')
    
    for(let i = 0; i < publicMusics.length; i++){
        pbMusic.push(publicMusics[i].outerHTML)
    }
    for(let i = 0; i < privateMusics.length; i++){
        pvMusic.push(privateMusics[i].outerHTML)
    }

    tradeMusics(pvMusic)
}

function selectOpiton(option){
    const options = document.getElementById('options').children
    switch (option){
        case 'pv':
            options[0].classList = 'select'
            options[1].classList = ''
            tradeMusics(pvMusic)
            break;
        case 'pb':
            options[1].classList = 'select'
            options[0].classList = ''
            tradeMusics(pbMusic)
        
    }
}

function tradeMusics(dataBase){
    const musicContainer = document.getElementById('musicsContainer')
    musicContainer.innerHTML = ''
    for(let i = 0; i < dataBase.length; i++){
        musicContainer.innerHTML += dataBase[i]
    }    
}

function submitForm(element){
    element.submit()
}