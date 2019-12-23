
// Retrieve dom elements
const scroller = document.querySelector("#scroller");
const template = document.querySelector('#track_template');
const sentinel = document.querySelector('#sentinel');


let counter = 0;

// Function to request new items and render to the dom
function loadItems() {
    fetch(`load?c=${counter}`).then((response) => {
        response.json().then((data) => {
            if (!data.length) {
                return;
            }
            for (let track of data) {
                // Clone the HTML template
                let templateClone = template.content.cloneNode(true);

                let trackElem = templateClone.querySelector(".track");
                trackElem.id = track['id'];
                trackElem.setAttribute('data-play', track['audio_url']);
                templateClone.querySelector("img").src = track['image_url'];

                // Append template to dom
                scroller.appendChild(templateClone);

                counter += 1;
            }
        })
    })
}

let intersectionObserver = new IntersectionObserver(entries => {
    // entries.forEach(entry => {
    //     console.log(entry.intersectionRatio);
    // });

    // If intersectionRatio is 0, the sentinel is out of view and we don't need to do anything
    if (entries[0].intersectionRatio <= 0) {
        return;
    }

    loadItems();
});

// Instruct the IntersectionObserver to watch the sentinel
intersectionObserver.observe(sentinel);


let mutationObserver = new MutationObserver(records => {
    setup();
    mutationObserver.disconnect();
});

// Instruct the MutationObserver to watch the scroller
mutationObserver.observe(scroller, { childList: true});
