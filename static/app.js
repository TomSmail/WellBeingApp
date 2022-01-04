function uploadFile(form){

  // Ininialise Form for Upload
  const formData = new FormData(form);

  // Output In HTML
  var output = document.getElementById("js_response")

  // Initialise Request
  var request = new XMLHttpRequest();
  request.open("POST", "run_script", true);

  request.onload = function(oEvent) {

        if (request.status == 200) {
          // Succesful Upload
          output.innerHTML = "Uploaded!";
          console.log(request.response)
  
        } 

        else if (request.status == 413) {
          // Return user understanable error
          output.innerHTML = "File Was Too Large!";
          console.log(request.response)
  
        } 

        else if (request.status == 404) {
          // Return user understanable error
          output.innerHTML = "A 404 Not Found!";
          console.log(request.response)
  
        } 
        
        else{
          // Return Specific Error 
          output.innerHTML = request.status;

        }
      };

      output.innerHTML = "Waiting!";
  console.log("Sending File!")
  request.send(formData);
}
