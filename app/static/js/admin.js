// websocket
const socket = io('http://localhost:8080')

socket.on('connect', () => {
    console.log('Conexão estabelecida com o servidor Socket.IO')
})

socket.on('conected_user_list', (data) => {
    console.log('ususarios conectados: ', data)
    updateUsersConnecteds(data)
})

socket.on('update_account_list', (data) => {
    updateUsers(data)
})

function updateUsers(data) {
    const allUsers = document.getElementById('allUsers')
    allUsers.innerHTML = ''

    for(let i = 0; i < data.length; i++) {
        let element = `<div onclick="selectUser(this)" class="us">
        <p class = "username">`+data[i]['name'] +`</p>`

        if (data[i]['admin']) {
            element += "<p>admin</p>"
        }
        else {
            element += "<p>user</p>"
        }
        if (!data[i]['connected']) {
            element += "<p class='connectedUser' style='color: rgb(255, 114, 114);'>desconectado</p></div>"
        } else {
            element += "<p class='connectedUser' style='color: rgb(191, 250, 103);'>conectado</p></div>"
        }
        allUsers.innerHTML += element
    }
}


function updateUsersConnecteds(data) {
    const connecteds = document.getElementById('connecteds')
    const allUsers = document.getElementById('allUsers')
    connecteds.innerHTML = ''

    for (let i = 0; i < data.length; i++) {
        if (data[i]['permision'] == true) {
            connecteds.innerHTML += '<li class="adm">' + data[i]['name'] + '</li>'
        }
        else {
            connecteds.innerHTML += '<li>' + data[i]['name'] + '</li>'
        }
    }

    for (let j = 0; j < allUsers.children.length; j++) {
        connectElement = allUsers.children[j].getElementsByClassName('connectedUser')[0]
        connectElement.innerHTML = 'desconectado'
        connectElement.style = 'color: rgb(255, 114, 114);'
        for (let i = 0; i < data.length; i++) {
            if (allUsers.children[j].getElementsByClassName('username')[0].innerHTML == data[i]['name']) {
                connectElement.innerHTML = 'conectado'
                connectElement.style = 'color: rgb(191, 250, 103);'
            }
        }
    }


}

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

async function removerUser() {
    if (userSelect != '') {
        let user = userSelect.children[0].innerHTML
        let ver = await postData('removeUser', user)
        if (ver == true) {
            userSelect.remove()
        }
        else {
            console.log('error ao remover usuario')
        }
    }
}

async function removeMusic() {
    musicsToRemove = document.getElementsByClassName('select')
    let rmMusic = []
    for (let i = 0; i < musicsToRemove.length; i++) {
        rmMusic.push(musicsToRemove[i].parentElement.children[2].children[0].innerHTML)
    }

    let ver = await postData('removeMusic', rmMusic)
    if (ver == true) {
        len = musicsToRemove.length
        for (let i = 0; i < len; i++) {
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
    } catch (error) {
        console.error('Erro:', error)
    }

}