function createSignInAlert(message, alertType) {
    var alertBox = document.getElementById('registerAlert');
    alertBox.style.cssText = 'position: fixed !important; top: 20% !important; z-index: 3 !important; width: 300px !important;' ;

  }

  function createDrawAlert(message, alertType) {
    var alertBox = document.getElementById('drawAlert');
    alertBox.style.cssText = 'position: fixed !important; top: 20% !important; z-index: 3 !important; width: 300px !important;' ;

  }
  

  function noSubmission() {
    createDrawAlert("You can't vote unless you submit a drawing!", 'alert-danger');
  }
  
  function notSignedIn() {
    createSignInAlert("You can't downvote as a guest user.", 'alert-warning');
  }

  function closeAlert() {
    var alertBox1 = document.getElementById('registerAlert');
    var alertBox2 = document.getElementById('drawAlert');
    
    // Add bounce-out animation class to the first alert box
    alertBox1.classList.add('bounce-out');
    
    // Add bounce-out animation class to the second alert box
    alertBox2.classList.add('bounce-out');
  
    // Wait for the animation to complete
    setTimeout(function() {
      // Hide the first alert box
      alertBox1.style.display = 'none';
      // Remove the bounce-out animation class
      alertBox1.classList.remove('bounce-out');
      
      // Hide the second alert box
      alertBox2.style.display = 'none';
      // Remove the bounce-out animation class
      alertBox2.classList.remove('bounce-out');
    }, 500);
  }
  

  document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('registerAlert').style.cssText = 'display: none !important';
    document.getElementById('drawAlert').style.cssText = 'display: none !important';
  });