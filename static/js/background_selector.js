  // Function to change the background
  function changeBackground() {
    var back = document.getElementById('back');
  
    // Define the different background classes
    var classes = ['isometric', 'zig-zag', 'zig-zag-3d', 'v-lines'];
  
    // Find the index of the current class in the array
    var currentIndex = -1;
    for (var i = 0; i < classes.length; i++) {
      if (back.classList.contains(classes[i])) {
        currentIndex = i;
        break;
      }
    }
  
    // If the current class was found, remove it
    if (currentIndex !== -1) {
      back.classList.remove(classes[currentIndex]);
    }
  
    // Calculate the index of the next class
    var nextIndex = (currentIndex + 1) % classes.length;
  
    // Add the next class
    back.classList.add(classes[nextIndex]);
  
    currentClass = classes[nextIndex];
  
    console.log(currentClass);
  
    // Set the selected background class as the value of the hidden input field
    document.getElementById('backgroundInput').value = currentClass;
  
    // Submit the hidden form
    document.getElementById('backgroundForm').submit();
  }