// firebase-delete-user.js

// Firebase configuration
var firebaseConfig = {
    apiKey: "AIzaSyAQkoqiC-C_QguqGkxzykJ8hRfx2eCtTWs",
    authDomain: "kodearrow-website.firebaseapp.com",
    databaseURL: "https://kodearrow-website-default-rtdb.firebaseio.com",
    projectId: "kodearrow-website",
    storageBucket: "kodearrow-website.appspot.com",
    messagingSenderId: "1076838775827",
    appId: "1:1076838775827:web:f7e249864699a6cea893e6",
    measurementId: "G-CCDRFW24ZL"
  };
  
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
  
  // Get a reference to the Firebase database
  const database = firebase.database();
  
  // Function to delete a user by user ID
  function deleteUser(userId) {
    const userRef = database.ref('users/' + userId);
    
    userRef.remove()
      .then(() => {
        console.log('User deleted successfully');
      })
      .catch((error) => {
        console.error('Error deleting user:', error.message);
      });
  }
  
  // Example usage: Call deleteUser function with a specific user ID
  const userIdToDelete = "user123"; // Replace with the actual user ID you want to delete
  deleteUser(userIdToDelete);
  