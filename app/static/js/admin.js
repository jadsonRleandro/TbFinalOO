function expand(element) {
    const container = document.getElementById('open')
    const elementContainer = document.getElementById('elements')
    const openTitel = document.getElementById('openTitle')

    if (element == "close") {
        container.style.display = 'none'
        elementContainer.innerHTML = ''
    }
    else {
        title = element.innerHTML
        data = element.parentElement.children[1]

        openTitel.innerHTML = title
        elementContainer.innerHTML = data.outerHTML

        container.style.display = 'inline'
    }
}

function select(element) {
    if (element.classList.contains("select")) {
        element.classList.remove("select")
    }
    else {
        element.classList.add("select")
    }
}

userSelect = ""

function selectUser(element) {
    if (userSelect != '') {
        userSelect.style = "background-color: none;"
    }
    userSelect = element
    userSelect.style = "background-color: rgb(41, 39, 39);"
}


document.getElementById('search').addEventListener('input', function () {
    const users = document.querySelectorAll('.us');

    users.forEach(userDiv => {
        const txt = userDiv.querySelector('p').textContent.toLowerCase();
        userDiv.style.display = txt.includes(this.value) ? '' : 'none';
    });
});


async function setAdmin() {
    if (userSelect != '') {
        let user = userSelect.children[0].innerHTML
        let ver = await postData('setAdmin', user)
        if (ver == true) {
            userSelect.children[1].innerHTML = 'admin'
        }
    }
}

async function removerUser(){
    if (userSelect != ''){
        let user = userSelect.children[0].innerHTML
        let ver = await postData('removeUser', user)
        if (ver == true){
            userSelect.remove()
        }
        else{
            console.log('error ao remover usuario')
        }
    }
}

async function removeMusic() {
    musicsToRemove = document.getElementsByClassName('select')
    let rmMusic = []
    for(let i = 0; i < musicsToRemove.length; i ++){
        rmMusic.push(musicsToRemove[i].parentElement.children[2].children[0].innerHTML)
    }

    let ver = await postData('removeMusic', rmMusic)
    if (ver == true){
        len = musicsToRemove.length
        for(let i = 0; i < len; i ++){
            musicsToRemove[0].parentElement.remove()
        }
    }
}

async function postData(paramet, datas) {
    let file = { 'paramet': paramet, 'data': datas }
    try {
        let res = await fetch('/admin', {
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