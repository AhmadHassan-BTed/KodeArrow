const projectID = process.env.FIREBASE_PROJECT_ID || 'kodearrow-server';
const scriptURL = `https://firestore.googleapis.com/v1/projects/${projectID}/databases/(default)/documents/payments`;
const form = document.forms['paymentFormName']
   
// Set the initial values for date and time fields on page load
const currentDate = new Date();
const formattedDate = currentDate.toISOString().split('T')[0];
const formattedTime = currentDate.toLocaleTimeString();
document.getElementById('date').value = formattedDate;
document.getElementById('time').value = formattedTime;

form.addEventListener('submit', async e => {
  e.preventDefault();
  
  const submitButton = document.querySelector('.submitButton');
  const originalButtonText = submitButton.value || 'submit';
  submitButton.value = 'Submitting...';
  submitButton.disabled = true;

  const fullName = document.getElementById('fullName').value;
  const phoneNo = document.getElementById('phoneNo').value;
  const email = document.getElementById('email').value;
  const bank = document.getElementById('bank').value;
  const accountNumber = document.getElementById('accountNumber').value;
  const screenshotFile = document.getElementById('uploadScreenshot').files[0];

  let screenshotBase64 = "";
  if (screenshotFile) {
    // Check if the file size is too large (Firestore doc size limit is 1MB)
    if (screenshotFile.size > 800 * 1024) {
      alert("Screenshot is too large. Please upload an image under 800 KB.");
      submitButton.value = originalButtonText;
      submitButton.disabled = false;
      return;
    }
    
    try {
      screenshotBase64 = await getBase64(screenshotFile);
    } catch (err) {
      console.error("Failed to read file", err);
    }
  }

  // Format data for Firestore REST API
  const firestoreData = {
    fields: {
      fullName: { stringValue: fullName },
      phoneNo: { stringValue: phoneNo },
      email: { stringValue: email },
      bank: { stringValue: bank },
      accountNumber: { stringValue: accountNumber },
      date: { stringValue: formattedDate },
      time: { stringValue: formattedTime },
      screenshot: { stringValue: screenshotBase64 }
    }
  };

  fetch(scriptURL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(firestoreData)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Failed to submit payment. Please verify your internet connection.');
    }
    tick();
  })
  .catch(error => {
    console.error('Error!', error.message);
    alert(error.message);
  })
  .finally(() => {
    submitButton.value = originalButtonText;
    submitButton.disabled = false;
  });
});

function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
}

function tick() {
  const section2 = document.querySelector('.reciptpaper2-icon');
  const payback = document.querySelector('.payback');
  const submitButton = document.querySelector('.submitButton');
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
  });

  // Reset the form fields
  form.reset();

  // Reset the upload label
  const fileInputLabel = document.getElementById('uploadScreenshot').parentElement;
  fileInputLabel.innerText = 'Choose File';

  // Hide date and time fields
  document.getElementById('date').style.display = 'none';
  document.getElementById('time').style.display = 'none';
}
