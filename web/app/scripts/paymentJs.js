const scriptURL = 'https://script.google.com/macros/s/AKfycbznN7rk_nRHkQVO4u5cngalKkaI8td3z3X7D47ZpDYtzbc0HfgtFbh4DLd5deKU7HaH/exec'
const form = document.forms['paymentFormName']
   
   // Set the initial values for date and time fields on page load
    const currentDate = new Date();
    const formattedDate = currentDate.toISOString().split('T')[0];
    const formattedTime = currentDate.toLocaleTimeString();
    document.getElementById('date').value = formattedDate;
    document.getElementById('time').value = formattedTime;
 
 form.addEventListener('submit', e => {
      e.preventDefault();
      
      // Update form data with the current date and time
      const formData = new FormData(form);
      formData.append('date', formattedDate);
      formData.append('time', formattedTime);
      
      fetch(scriptURL, { method: 'POST', body: new FormData(form)})
    .then(response =>  tick()
    // alert("Thanks for Contacting us..! We Will Contact You Soon...")
    )
    .catch(error => console.error('Error!', error.message))
});
    
function tick() {
  const section2 = document.querySelector('.reciptpaper2-icon');
  const payback = document.querySelector('.payback');
  const submitButton = document.querySelector('.submitButton');
  // Check the viewport width
  const viewportWidth = window.innerWidth || document.documentElement.clientWidth;
  
  
  setTimeout(function() {
    
if (viewportWidth > 600) {
  setTimeout(function() {
    section2.style.marginTop = '2vw';
    payback.style.marginTop = '3vw';
    submitButton.style.marginTop = '2.2vw';
  }, -40);
} else {
  setTimeout(function() {
    section2.style.marginTop = '10vw';
    payback.style.marginTop = '14vw';
    submitButton.style.marginTop = '12vw';
  }, -40);
}
    // section2.style.marginTop = '2vw';
    // payback.style.marginTop = '3vw';
    // submitButton.style.marginTop = '2.2vw';
  });

// Clear form fields
// $("#myForm")[0].reset();    
  
  // Hide date and time fields
  document.getElementById('date').style.display = 'none';
  document.getElementById('time').style.display = 'none';
}
