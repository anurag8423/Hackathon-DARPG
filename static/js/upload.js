function downloadFile(filePath) {
    // Create a hidden anchor element
    var downloadLink = document.getElementById('download-btn');

    // Set the href attribute to the file path
    downloadLink.href = '/download/?file=' + encodeURIComponent(filePath);

    // Set the download attribute to specify the filename
    downloadLink.setAttribute('download', '');

    // Trigger a click event on the anchor element
    downloadLink.click();
}
function buffer(){
    console.log("buffer reached")
    var buffer=document.getElementById('buffer')
    buffer.style.display='block';
}