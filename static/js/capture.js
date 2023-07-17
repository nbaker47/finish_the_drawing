 // Function to capture the HTML as an image
 /*
function share(id) {

var cardId = 'card-' + id

console.log(cardId)

html2canvas(document.getElementById(cardId), {
    allowTaint: true // Enable capturing cross-origin images
  }).then(function (canvas) {
    // Convert canvas to data URL
    var base64image = canvas.toDataURL("image/png");

    // Create a link element
    var downloadLink = document.createElement("a");
    downloadLink.href = base64image;

    // Set the "download" attribute to specify the filename
    downloadLink.download = "image.png";

    // Programmatically click the link to trigger the download
    downloadLink.click();
});
}
*/

function share(id) {
    var imageId = 'image-' + id;
    var image = document.getElementById(imageId);
    
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    
    canvas.width = image.width;
    canvas.height = image.height;
    
    context.drawImage(image, 0, 0);
    
    canvas.toBlob(function(blob) {
      var file = new File([blob], 'image.png', { type: 'image/png' });
      var filesArray = [file];
    
      if (navigator.canShare && navigator.canShare({ files: filesArray })) {
        navigator.share({ files: filesArray })
          .then(() => console.log('Image shared successfully.'))
          .catch((error) => console.error('Error sharing image:', error));
      } else {
        console.log('Sharing files not supported in this browser.');
        // Fallback code for browsers that do not support file sharing
        // You can replace this with your custom sharing logic (e.g., displaying a share dialog).
        var newTab = window.open(image.src);
      }
    }, 'image/png');
  }
  