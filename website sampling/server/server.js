const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const admin = require('firebase-admin');
require('dotenv').config();

// Initialize Firebase Admin SDK with service account key
const serviceAccount = require('./kodearrow-website-167ead05474a.json'); // Adjust path as necessary
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://kodearrow-website-default-rtdb.firebaseio.com"
});

// Middleware to parse JSON bodies
app.use(bodyParser.json());

// Endpoint to handle form submissions
app.post('/submitForm', (req, res) => {
  const formData = req.body;

  // Validate formData if necessary

  // Save data to Firebase
  const db = admin.database();
  db.ref('submissions').push(formData)
    .then(() => {
      res.status(200).json({ status: 'success', message: 'Data received and processed successfully' });
    })
    .catch(error => {
      console.error('Error saving data to Firebase:', error);
      res.status(500).json({ status: 'error', message: 'Error processing data' });
    });
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
