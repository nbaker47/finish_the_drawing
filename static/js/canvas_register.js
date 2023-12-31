
// Define a counter variable to keep track of the number of strokes
var strokeCounter = 0;

// Variables for canvas and drawing
var canvas = document.getElementById('drawing-canvas');
var context = canvas.getContext('2d');

var isDrawing = false;
var isFirstTouch = true; // Flag to differentiate between first touch and random lines
var userDrawings = []; // Array to store user's drawings
var currentLine = null; // Variable to store the current line segment

// Event listeners for drawing
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);

// Touch event listeners for drawing
canvas.addEventListener('touchstart', startDrawing);
canvas.addEventListener('touchmove', draw);
canvas.addEventListener('touchend', stopDrawing);

// Update the text in the pencil-text element
function updatePencilText() {
    var pencilText = document.getElementById('pencil-text');
    var pencilImage = document.getElementById('pencil-image');
    var currentText = pencilText.textContent;

    // Array of different texts to cycle through
    // var gptDescriptions_1 = ['Be Creative!', 'Keep going!', 'Nice job!', 'Almost there!', 'You got this!'];
    var gptDescriptions_1 = [
    "You look amazing today!",
    " You're a smart cookie.",
    "I bet you make babies smile.",
    "You have impeccable manners.",
    "I like your style.",
    "You have the best laugh.",
    "I appreciate you.",
    ];


    // Update the text every 3 strokes
    if (strokeCounter % 3 === 0) {

    // Random index
    var randomIndex = Math.floor(Math.random() * gptDescriptions_1.length);
    
    // Apply animation class to the speech bubble
    pencilText.classList.add('bubble-animation');
    
    
    // Set the new text after a short delay to allow the animation to play
    setTimeout(function() {

        if (strokeCounter < 5){
        // Set the new text
        pencilText.textContent = gptDescriptions_1[randomIndex];
        } else if (strokeCounter == 10){
        // Set the new text
        pencilText.textContent = gptDescriptions_1[randomIndex];
        pencilImage.classList.add('bubble-animation');
        pencilImage.src = "/static/media/pencil_happy.png";
        }
        else if (strokeCounter > 10){
        // Set the new text
        pencilText.textContent = gptDescriptions_1[randomIndex];
        pencilImage.src = "/static/media/pencil_happy.png";
        }

    }, 200); // Adjust the delay as needed
    
    // Remove the animation class after the animation completes
    setTimeout(function() {
        pencilText.classList.remove('bubble-animation');
        pencilImage.classList.remove('bubble-animation');
    }, 1000); // Adjust the duration of the animation
    
    }

    // Increment the stroke counter
    strokeCounter++;
}

// Get the scale factor for transforming screen space to canvas space
function elementScale() {
    let el = canvas;
    return el.width / el.offsetWidth;
}

// Get cursor coordinates
function getXY() {
    let rect = canvas.getBoundingClientRect();
    let x_temp, y_temp;

    if (event.type.startsWith('touch')) {
    x_temp = (event.touches[0].clientX - rect.left) * elementScale();
    y_temp = (event.touches[0].clientY - rect.top) * elementScale();
    } else {
    x_temp = (event.clientX - rect.left) * elementScale();
    y_temp = (event.clientY - rect.top) * elementScale();
    }

    return [x_temp, y_temp];
}


// Start drawing function
function startDrawing(event) {
    event.preventDefault(); // Prevent scrolling on touch devices
    isDrawing = true;

    // Get the coordinates of the cursor
    let [x_temp, y_temp] = getXY();
    // console.log(x_temp, y_temp);

    // Set the starting point of the line segment
    currentLine = {
    points: [{ x: x_temp, y: y_temp }],
    };
}



// Draw on the canvas
function draw(event) {
    // Get the coordinates of the cursor
    let [x_temp, y_temp] = getXY();
    // console.log(x_temp, y_temp);

    if (!isDrawing) return;

    // Check if the current line segment intersects with any of the random lines
    // var isIntersecting = checkIntersection(currentLine.points[0].x, currentLine.points[0].y, x_temp, y_temp);

    context.lineWidth = 5;
    context.lineCap = 'round';

    currentLine.points.push({ x: x_temp, y: y_temp });

    // clear the canvas
    context.clearRect(0, 0, canvas.width, canvas.height);
    // redraw random lines:
    // drawRandomLines();

    userDrawings.forEach(function (line) {
        context.beginPath();
        context.moveTo(line.points[0].x, line.points[0].y);
        for (var i = 1; i < line.points.length; i++) {
            context.lineTo(line.points[i].x, line.points[i].y);
        }
        context.stroke(); 
    });

    context.beginPath();
    context.moveTo(currentLine.points[0].x, currentLine.points[0].y);
    for (var i = 1; i < currentLine.points.length; i++) {
        context.lineTo(currentLine.points[i].x, currentLine.points[i].y);
    }
    context.stroke();
}


// Stop drawing
function stopDrawing() {
    if (!isDrawing) return;
    isDrawing = false;
    // Store the completed line segment in the userDrawings array
    userDrawings.push(currentLine);
    // Call the updatePencilText function
    updatePencilText();
}

// Undo the last line segment drawn by the user
function undoLastStroke() {

    console.log("undoing stroke");

    // Remove the last line segment from the userDrawings array
    userDrawings.pop();

    // Clear the canvas
    context.clearRect(0, 0, canvas.width, canvas.height);
    // redraw random lines:
    // drawRandomLines();

    // Redraw all the user's line segments
    userDrawings.forEach(function (line) {
    context.beginPath();
    context.moveTo(line.points[0].x, line.points[0].y);
    for (var i = 1; i < line.points.length; i++) {
        context.lineTo(line.points[i].x, line.points[i].y);
    }
    context.stroke();
    });
}