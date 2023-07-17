  // Function to create the delete alert box
  function createDeleteAlert(message, alertType) {
    var alertBox = document.getElementById('deleteAlert');
    alertBox.style.cssText = 'position: fixed !important; top: 20% !important; z-index: 3 !important; width: 300px !important;';
  }

  // Function to show delete confirmation alert
  function deleteConfirm(id) {
    document.getElementById('final-delete-button').value = id;
    createDeleteAlert("You can't vote unless you submit a drawing!", 'alert-danger');
  }

  // Function to close the delete alert box
  function closeAlert() {
    var alertBox1 = document.getElementById('deleteAlert');
    
    // Add bounce-out animation class to the first alert box
    alertBox1.classList.add('bounce-out');
    
    // Wait for the animation to complete
    setTimeout(function() {
      // Hide the first alert box
      alertBox1.style.display = 'none';
      // Remove the bounce-out animation class
      alertBox1.classList.remove('bounce-out');
    }, 500);
  }

  // When the DOM is loaded
  document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('deleteAlert').style.cssText = 'display: none !important';
  });

  