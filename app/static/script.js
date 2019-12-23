
// Retrieve dom elements
const currentImg = document.getElementById('current_img');
const playBtn = document.getElementById('play');
const audio = document.getElementById('player');
const source = document.getElementById('audioSource');


// Button Controls //

function setPauseIcon() {
    playBtn.classList.remove('glyphicon-play');
    playBtn.classList.add('glyphicon-pause');
}
function setPlayIcon() {
    playBtn.classList.add('glyphicon-play');
    playBtn.classList.remove('glyphicon-pause');
}

function playAudio() {
    audio.play();
    setPauseIcon();
}
function pauseAudio() {
    audio.pause();
    setPlayIcon();
}

function buttonPlay() {
    if (audio.paused) {
        playAudio();
    } else {
        pauseAudio();
    }
}


// Changing Track //

let currentTrack = null;


function setCurrentTrack(newTrack) {
    currentTrack = newTrack;

    // Set cover image
    let img = currentTrack.querySelector('img');
    currentImg.src = img.src;

    // Set audio source
    source.src = currentTrack.getAttribute('data-play');

    // Load audio
    audio.load();
}
function playThisTrack(track) {
    setCurrentTrack(track);
    playAudio();
}

function playPrev() {
    let track = document.querySelector('.track.done:last-child');
    if (track) {
        track.classList.remove('done');
        playThisTrack(track);
    }
}

function playNext() {
    if (currentTrack) {
        currentTrack.classList.add('done');
    }

    let track = document.querySelector('.track:not(.done)');
    if (track) {
        playThisTrack(track);
    } else {
        console.log('No next track')
    }
}

// Initialize with first track
function setup() {
    let track = document.querySelector('.track');
    setCurrentTrack(track);
}

audio.onended = function () {
    playNext();
};


// Keyboard Controls //

document.addEventListener("keydown", function(e) {
    // Play/pause controlled by space
    if (e.code === 'Space') {
        e.preventDefault();
        buttonPlay();
    } else if (e.code === 'ArrowRight') {
        playNext();
    } else if (e.code === 'ArrowLeft') {
        playPrev();
    }
});


