function select(element){
    if (element.classList.contains("select")){
        element.classList.remove("select")
    }
    else{
        element.classList.add("select")
    }
}

function rm(){
    musicsToRemove = document.getElementsByClassName('select')
    let rmMusic = []
    for(let i = 0; i < musicsToRemove.length; i ++){
        rmMusic.push(musicsToRemove[i].parentElement.children[2].children[0].innerHTML)
    }

    fetch('/remove', {
        method: 'post',
        headers:{'content-Type': 'application/json'},
        body: JSON.stringify(rmMusic)
    }).then(response => response.json())
    .then(data => {
        loadNewDB(data)
      console.log('Resposta do servidor:', data)
    })
    .catch(error => console.error('Erro:', error))

    confirmRemove('close')
}

function loadNewDB(db){
    const musicContainer = document.getElementById('musicsContainer')
    musicContainer.innerHTML = ''

    for(let i = 0; i < db.length; i++){
        musicContainer.innerHTML += `<div class="musics">
                    <div onclick="select(this)" class="square"></div>
                    <img class="musicImg" src="`+ db[i]['thumb'] +`">
                    <div class="musicInfos">
                        <p class="musicName">`+ db[i]['name']+`</p>
                        <p class="artist">`+ db[i]['artist']+`</p>
                    </div>
        </div>`
    }
}

function returnToMenu(){
    const form = document.getElementById('options')
    form.submit()
}

function confirmRemove(paramet){
    const confirmContainer = document.getElementById('confirm')
    switch (paramet){
        case 'open':
            confirmContainer.style.display = 'inline'
            break;
        case 'close':
            confirmContainer.style.display = "none"
            break;
    }
}