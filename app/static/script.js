
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
    if (currentTrack) {
        let track = currentTrack.previousElementSibling;
        if (track) {
            track.classList.remove('done');
            playThisTrack(track);
        }
    }
}

function playNext() {
    if (currentTrack) {
        currentTrack.classList.add('done');

        // If we can, play the next track after currentTrack
        let track = currentTrack.nextElementSibling;
        if (track) {
            track.classList.remove('done');
            playThisTrack(track);
            return;
        }
    }

    // Otherwise, play the first track that hasn't already been played
    let track = document.querySelector('.track:not(.done)');
    if (track) {
        playThisTrack(track);
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


// Progress Bar

function initProgressBar() {
    if (audio.currentTime) {
        progressBar.value = (audio.currentTime / audio.duration);
        progressBar.addEventListener("click", seek);
    }

    function seek(event) {
        let percent = event.offsetX / this.offsetWidth;
        audio.currentTime = percent * audio.duration;
        progressBar.value = percent / 100;
    }
}


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



// Shuffle tracks

function shuffle() {
    // Fisher-Yates shuffle
    for (let i = scroller.children.length; i >= 0; i--) {
        scroller.appendChild(scroller.children[Math.random() * i | 0]);
    }
}
