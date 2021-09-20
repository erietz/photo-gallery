let start = window.sessionStorage.getItem("start");
let stop = window.sessionStorage.getItem("stop");

if (typeof start === "undefined" || start === null) {
    window.sessionStorage.setItem("start", 0)
}

if (typeof stop === "undefined" || stop === null) {
    window.sessionStorage.setItem("stop", 10)
}

function load_next() {
    start = parseInt(window.sessionStorage.getItem("start"));
    stop = parseInt(window.sessionStorage.getItem("stop"));

    start += 10;
    stop += 10;

    window.sessionStorage.setItem("start", start)
    window.sessionStorage.setItem("stop", stop)
    window.location.href = `/?start=${start}&stop=${stop}`
    console.log('start', start, 'stop', stop)
}

function load_previous() {
    start = parseInt(window.sessionStorage.getItem("start"));
    stop = parseInt(window.sessionStorage.getItem("stop"));

    start -= 10;
    stop -= 10;

    window.sessionStorage.setItem("start", start)
    window.sessionStorage.setItem("stop", stop)
    window.location.href = `/?start=${start}&stop=${stop}`
    console.log('start', start, 'stop', stop)
}

document.addEventListener('keydown', (event) => {
    switch (event.key) {
        case 'Escape':
            do_close();
            break;
        case 'ArrowRight':
            next_image();
            break;
    }
});
