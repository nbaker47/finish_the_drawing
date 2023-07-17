// make it fit inside footer by shrikning font size
function shrinkTextToFit(element) {
    const maxFontSize = 12; // Maximum font size in pixels
    const minFontSize = 10; // Minimum font size in pixels

    let fontSize = maxFontSize;
    element.style.fontSize = fontSize + "px";
    
    while (element.scrollHeight > element.offsetHeight && fontSize > minFontSize) {
        fontSize--;
        element.style.fontSize = fontSize + "px";
    }
    
    // Check if the text still overflows after reducing the font size
    if (element.scrollWidth > element.offsetWidth) {
        const scaleFactor = element.offsetWidth / element.scrollWidth;
        fontSize = Math.floor(fontSize * scaleFactor);
        element.style.fontSize = fontSize + "px";
    }
    }

    //shrink footer text to fit
    const cardFooters = document.getElementsByClassName("card-footer");
    // Set random descriptions for each span element
    for (let i = 0; i < cardFooters.length; i++) {
    shrinkTextToFit(cardFooters[i]);
    }