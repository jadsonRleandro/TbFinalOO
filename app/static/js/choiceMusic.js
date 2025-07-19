const audio = document.getElementById("musicAudio");
const progress = document.querySelector('.progress');
const progressBar = document.querySelector('.progressBar');
const currentTime = document.querySelector('.currentTime');
const duration = document.querySelector('.duration');
const volumeSlider = document.querySelector('.volumeSlider');

audio.ontimeupdate = updateTime;
volumeSlider.onchange = setVolume;

progressBar.addEventListener('click', (e) => {
    const width = progressBar.clientWidth;
    const clickX = e.offsetX;
    const duration = audio.duration;
    audio.currentTime = (clickX / width) * duration;
});


function tradeBtn(button) {
    const playIconPath = "/static/assets/playIcon.png";
    const pauseIconPath = "/static/assets/pauseIcon.png";
    musicBtn = document.getElementsByClassName('play-music')

    if (audio.paused) {
        audio.play();
        button.src = pauseIconPath;
    } else {
        audio.pause();
        button.src = playIconPath;
    }
}


function updateTime() {
    const currentMinutes = Math.floor(audio.currentTime / 60);
    const currentSeconds = Math.floor(audio.currentTime % 60);
    currentTime.textContent = currentMinutes + ":" + formatZero(currentSeconds);

    const durationFormatted = isNaN(audio.duration) ? 0 : audio.duration;
    const durationMinutes = Math.floor(durationFormatted / 60);
    const durationSeconds = Math.floor(durationFormatted % 60);
    duration.textContent = durationMinutes + ":" + formatZero(durationSeconds);

    const progressWidth = durationFormatted ? (audio.currentTime / durationFormatted) * 100 : 0;
    progress.style.width = progressWidth + "%";
}

function setVolume() {
    audio.volume = volumeSlider.value / 100;
}

const formatZero = (n) => (n < 10 ? "0" + n : n);
