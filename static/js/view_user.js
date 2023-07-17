function viewUser(user){
    // Create a form and append the image data
    var form = document.createElement('form');
    form.action = '/view-profile';
    form.method = 'POST';
    // form.enctype = 'multipart/form-data'; // Set the enctype attribute

    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'username';
    input.value = user;

    form.appendChild(input);
    document.body.appendChild(form);

    // Submit the form
    form.submit();
  }