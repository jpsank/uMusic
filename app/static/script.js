
const currentImg = document.getElementById('current_img');
const playBtn = document.getElementById('play');
const audio = document.getElementById('player');
const source = document.getElementById('audioSource');

function setPauseIcon() {
    playBtn.classList.remove('glyphicon-play');
    playBtn.classList.add('glyphicon-pause');
}
function setPlayIcon() {
    playBtn.classList.add('glyphicon-play');
    playBtn.classList.remove('glyphicon-pause');
}

function setCurrentTrack(trackElem) {
    // Set cover image
    let img = trackElem.querySelector('img');
    currentImg.src = img.src;

    // Set audio source
    source.src = trackElem.getAttribute('data-play');

    // Load and play audio
    audio.load();
    audio.play();
    setPauseIcon();
}

function playButton() {
    if (audio.paused) {
        audio.play();
        setPauseIcon();
    } else {
        audio.pause();
        setPlayIcon();
    }
}

function nextButton() {

}

function prevButton() {

}

