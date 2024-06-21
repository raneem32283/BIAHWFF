function boxAdd(){
    const formData = {
        wight: document.getElementById("box_wight").value,
        value: document.getElementById("value").value,
        city: document.getElementById("city").value,
      };
      
      // Make a POST request using the Fetch API
      fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })
      const formDataTrack = {
        wight: document.getElementById("Track_wight").value,
      };
}

  function trackAdd(){
   
      
      // Make a POST request using the Fetch API
      fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formDataTrack),
      })
  }
let boxes
  fetch('https://api.example.com/data')
  .then(response => response.json())
  .then(data => boxes
  )
  .catch(error => alert.error('Error:', error));
  boxes.forEach(box => {
    document.getElementById("box").hidden=true
    document.getElementById("box").value=box
  });