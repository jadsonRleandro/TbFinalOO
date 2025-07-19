// INNIT
updateBars()

window.addEventListener('resize', function () {
    updateBars()
});



function updateBars() {
    let bar = `<div style = "height: 100%;" class="bar"></div>` // criando uma barra generica
    let barUp = document.getElementsByClassName('conjbar')[1] // pegando a div que tem as barras superiores
    // resetando o html das barras 
    barUp.innerHTML = ''

    // add barras relativa ao tamanho da tela
    let qBar = Math.round(window.innerWidth / 5) // quantidade de barras que vao cabe na tela
    for (let i = 0; i < qBar; i++) {
        seconds = Math.round(randomNumber(4, 2))
        bar = `<div style = "max-height:` + randomNumber(100,30) +`%; animation: barsUp `+ seconds+`s infinite;" class="bar actvanimation"></div>`
        barUp.innerHTML += bar
    }
}

function randomNumber(max, min) { // retorna numero aleatorio no range de max - min
    let randomNumber = Math.round(Math.random() * (max - min + 1) + min)

    return randomNumber
}