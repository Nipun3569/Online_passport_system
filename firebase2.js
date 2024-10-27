const firebaseConfig = {
  apiKey: "AIzaSyA-sampleApiKey1234567890abcdefg", 
  authDomain: "passport-seva-app.firebaseapp.com",
  databaseURL: "https://passport-seva-app.firebaseio.com",
  projectId: "passport-seva-app",
  storageBucket: "passport-seva-app.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdef1234567890abcdef"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Reference the Firebase Realtime Database
var contactFormDB = firebase.database().ref("contactForm");

// Add an event listener for the form submission
document.getElementById("contactForm").addEventListener("submit", submitForm);

function submitForm(e) {
  e.preventDefault();

  // Get form values from the HTML inputs
  var email = getElementVal("name"); 
  var fullName = getElementVal("fullname");
  var dob = getElementVal("birthday");
  var office = getElementVal("passportOffice");
  var password = getElementVal("password");
  var confirmPassword = getElementVal("confirmPassword");
  var preference = document.querySelector('input[name="account"]:checked').value; 

  // Basic password matching validation
  if (password !== confirmPassword) {
    showAlert("Passwords do not match!", "error");
    return;
  }

  // Save the form data to Firebase
  saveMessages(email, fullName, dob, office, preference)
    .then(() => {
      // Show success alert
      showAlert("Your details have been submitted successfully!", "success");

      // Reset the form after submission
      document.getElementById("contactForm").reset();
    })
    .catch((error) => {
      // Show error alert if something goes wrong
      showAlert("Error submitting form: " + error.message, "error");
    });
}

// Function to save data to Firebase
const saveMessages = (email, fullName, dob, office, preference) => {
  var newContactForm = contactFormDB.push(); // Create a new entry in the database

  return newContactForm.set({
    email: email,
    fullName: fullName,
    dateOfBirth: dob,
    passportOffice: office,
    preference: preference,
    timestamp: new Date().toISOString(), 
  });
};


const getElementVal = (id) => {
  return document.getElementById(id).value;
};

function showAlert(message, type) {
  const alertBox = document.querySelector(".custom-alert");
  alertBox.textContent = message;

  
  alertBox.style.backgroundColor = type === "success" ? "#4CAF50" : "#f44336";
  alertBox.style.display = "block";


  setTimeout(() => {
    alertBox.style.display = "none";
  }, 3000);
}
