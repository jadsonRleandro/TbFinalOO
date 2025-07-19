// websocket
const socket = io('http://localhost:8080')

socket.on('connect', () => {
    console.log('Conexão estabelecida com o servidor Socket.IO')
})

// load inicial
const username = document.getElementById('username').innerHTML
const avatar = document.getElementById('avatar').src

document.body.style.overflow = "hidden"

const load = document.getElementById("load")
load.addEventListener("animationend", (event) => {
    load.innerHTML = ""
    load.style = "    width: 0px; height: 0px;"
    document.body.style.overflow = "auto"
})

// funçao quando clica no play

let actMusic = ''
let db
let footerMusic = 'close'


const pauseIcon = "/static/assets/pauseIcon.png"
const playIcon = "/static/assets/playIcon.png"


async function play(self) {
    const footer = document.getElementById('footer')
    if (footerMusic == 'close'){
        footer.innerHTML = `<audio id="musicAudio"></audio>
            <form action="/music" method="get" onclick="submit()" id="actMusicInfos">
                <p class="musicName">Nome da Musica</p>
                <p class="artist">nome do artista</p>
            </form>
            <div id="controllers">
                <input type="button" class="arrows rotate180">
                <div class="playBtn">
                    <img id="actBtn" onclick="tradeBtn(this)" class="pauseIcon" src="/static/assets/pauseIcon.png">
                </div>
                <input type="button" class="arrows">
            </div>`

        footer.style = `width: 100vw;
                        animation: openFooter forwards 1s;`
        footerMusic = 'open'
    }

    const actBtn = document.getElementById('actBtn')


    musicName = self.parentElement.getElementsByClassName("musicName")[0].innerHTML 
    musicArtis = self.parentElement.getElementsByClassName("artist")[0].innerHTML 
    musicId = musicName
    musicBtn = document.getElementById(musicName).getElementsByClassName('playBtn')[0].children[0]
    
    if(self.children[0].classList[0] == 'playIcon'){
        db = document.getElementsByClassName('select')[0].innerHTML
        musicPath = await postData(db,musicName)

        infos = document.getElementById('actMusicInfos')

        infos.getElementsByClassName("musicName")[0].innerHTML = musicName
        infos.getElementsByClassName("artist")[0].innerHTML = musicArtis


        const audio = document.getElementById('musicAudio')
        fileName = encodeURIComponent(musicPath)
        audio.src = `controllers/musicsfiles/${musicPath}`
        audio.play()
    }

    if (actMusic != '' && actMusic != self.children[0]) {
        actMusic.src = playIcon
        actMusic.className = 'playIcon'
    }

    actMusic = self.children[0]

    tradeBtn(musicBtn)
}

function tradeBtn(btn){
    const audio = document.getElementById('musicAudio')

    if (btn.classList[0] == 'pauseIcon') {
        musicBtn.src = playIcon
        musicBtn.className = 'playIcon'
        actBtn.src = playIcon
        actBtn.className = 'playIcon'
        audio.pause()
    }
    else {
        musicBtn.src = pauseIcon
        musicBtn.className = 'pauseIcon'
        actBtn.src = pauseIcon
        actBtn.className = 'pauseIcon'
        audio.play()
    } 
}





async function postData(paramet, datas) {
    let file = { 'paramet': paramet, 'data': datas }
    try {
        let res = await fetch('/music', {
            method: 'post',
            headers: { 'content-Type': 'application/json' },
            body: JSON.stringify(file)
        })

        let data = await res.json()
        return data
    } catch(error){
        console.error('Erro:', error)    
    }
    
}
// abrindo e fechando o menu

let menuGui = 0

function openMenu() {
    const menu = document.getElementById('menu')
    let permision

    fetch('/permision', {
        method: 'get'
    }).then(response => response.json())
        .then(data => {
            permision = data
            if (menuGui == 0) {
                menuGui = 1
                menu.style = "height: 100vh; width: 40%;"
                menu.innerHTML = `        
        <div id="userInfos">
            <img onclick="openMenu()" id="avatar" src="`+ avatar +`" alt="avatar">
            <h1 id="username">`+ username + `</h1>
        </div>
        <br>
        <br>
        <br>
        <form class="menuOption" onclick="submitForm(this)" action = '/adicionarMusicas'>Adicionar Musica</form>
        <form onclick = "submitForm(this)" action = "/remove" method = "get" class="menuOption">Remover Musica</form>
        <form class="menuOption" onclick="submitForm(this)" action = '/conta'">Conta</form>
        
        <div onclick = "window.location.href='/logout'" id = "logout">
            LOGOUT<img src="./static/assets/exitIcon.png">
        </div>`

                if (permision) {
                    console.log(permision)
                    menu.innerHTML += `<form onclick = "submitForm(this)" action = "/admin" method = "get" class="menuOption">Admin</form>`
                }

            } else {
                menuGui = 0
                menu.innerHTML = ''
                menu.style = "height: 0px; width:0px"
            }
        })
        .catch(error => console.error('Erro:', error))
}


    
window.onload = getMusic()

function getMusic() {
    pbMusic = []
    pvMusic = []
    const publicMusics = document.getElementsByClassName('public')
    const privateMusics = document.getElementsByClassName('private')

    for (let i = 0; i < publicMusics.length; i++) {
        pbMusic.push(publicMusics[i].outerHTML)
    }
    for (let i = 0; i < privateMusics.length; i++) {
        pvMusic.push(privateMusics[i].outerHTML)
    }

    tradeMusics(pvMusic)
}

function selectOpiton(option) {
    const options = document.getElementById('options').children
    switch (option) {
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

function tradeMusics(dataBase) {
    const musicContainer = document.getElementById('musicsContainer')
    musicContainer.innerHTML = ''
    for (let i = 0; i < dataBase.length; i++) {
        musicContainer.innerHTML += dataBase[i]
    }
}

function submitForm(element) {
    element.submit()
}

document.getElementById('search').addEventListener('input', function () {
    const users = document.querySelectorAll('.musics');

    users.forEach(userDiv => {
        const txt = userDiv.querySelector(".musicName").textContent.toLowerCase();
        userDiv.style.display = txt.includes(this.value) ? '' : 'none';
    });
});

