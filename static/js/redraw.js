const passWarn = document.getElementById('passWarn');
passWarn.style.display = 'none';

// Execute code when the page finishes loading
window.addEventListener('load', function() {
    // Reload the page
    passWarn.style.display = 'none';
});

// Get the canvas element
    
// Get the submit button
const submitButton = document.getElementById('submit-button');

// Add event listener to the submit button
submitButton.addEventListener('click', () => {

    console.log('Submit button clicked.')

    // Get the drawing data (as base64 image data)
    const drawingData = canvas.toDataURL();

    // Check if the canvas has any drawn content
    if (strokeCounter < 1) {
        passWarn.style.display = 'block';
        passWarn.innerHTML = 'Please draw something.';
        return;
    }

    // Create a hidden input element to store the drawing data
    const hiddenInput = document.createElement('input');
    hiddenInput.setAttribute('type', 'hidden');
    hiddenInput.setAttribute('name', 'drawingData');
    hiddenInput.setAttribute('value', drawingData);

    // Append the hidden input to the form
    const form = document.querySelector('form');
    form.appendChild(hiddenInput);
    form.submit();
});
