

function upload() {
    const fileInput = document.getElementById('fileInput');
    const thumb = document.getElementById('thumb')
    const checkbox = document.getElementById('privado-check')
    let artista = document.getElementById('artista-id')
    const fileName = fileInput.files[0].name;
    
    let verification = 0;

    if(!fileInput.files.length) {
        alert('Selecione um arquivo MP3!');
        verification = 1;
        return;
    }
    if(!thumb.files.length) {
        alert('Selecione uma thumb para a música!.')
        verification = 1;
        return;
    }

    if(artista.value == '') {
        alert('Digite o nome do artista!.')
        verification = 1;
        return;
    }

    if (verification == 0) {
        let form = document.getElementById('container')
        form.submit()
    }
    
    
}

function returnToMenu(){
    const form = document.getElementById('options')
    form.submit()
}