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

    returnToMenu()
}

function returnToMenu(){
    const form = document.getElementById('options')
    form.submit()
}