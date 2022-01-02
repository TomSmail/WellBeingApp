window.onload = function() {

    var myForm = document.getElementById("myForm");

    myForm.onsubmit = function(event) {

    event.preventDefault;

    var myFile = document.getElementById("myFile");
    
    var mySubmit = document.getElementById("submit");
    
    var files = myFile.files;
    
    var formData = new FormData();

    formData.append("myFile", files[0], files[0].name);
    
    var xhr = new XMLHttpRequest();
    
    xhr.open("POST", "/upload", true);
    
    xhr.onload = function () {
        
        if (xhr.status === 200) {
        
        alert("File successfully uploaded")
        
        } else {
        
        alert("File upload failed!");
        
        }
        
        };
        
        xhr.send(formData);
        
        }
        
        };