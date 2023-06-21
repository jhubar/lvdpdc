
(function () {
  // "use strict";

  // let forms = document.querySelectorAll('.php-email-form');

  // Get the form element
  const contactForm = document.getElementById('contact-form');
  const bookForm = document.getElementById('book-form');
  // Get the loading, error, and success message elements
  const loadingMessage = document.getElementById('loading');



  bookForm.addEventListener('submit', function (event) {
    // Prevent the form from submitting
    event.preventDefault();

    // Show loading message
    loadingMessage.style.display = 'block';
    // Hide error message if previously shown


    // Perform form validation for book form
    if (validateBookForm()) {
      bookForm.submit();
      // Show success message

      // alert("Your booking has been submitted. We will contact you shortly.");

      bookForm.reset();
    } else {
      // Show error message
      errorMessage.style.display = 'block';
    }

  });

  // Add event listener for form submission
  contactForm.addEventListener('submit', function (event) {
    // Prevent the form from submitting
    event.preventDefault();

    // Perform form validation
    if (validateForm()) {
      // If the form is valid, submit it to Formspree
      contactForm.submit();
    }
  });


  // Function to validate the form fields
  function validateForm() {
    // Get the form inputs
    const nameInput = document.getElementById('name-contact-form');
    const emailInput = document.getElementById('email-contact-form');
    const subjectInput = document.getElementById('subject-contact-form');


    // Validate each field
    if (nameInput.value === '') {
      alert('Please enter your name.');
      return false;
    }

    if (emailInput.value === '') {
      alert('Please enter your email.');
      return false;
    }

    if (subjectInput.value === '') {
      alert('Please enter the subject.');
      return false;
    }



    return true;
  }

  // Function to validate the book form fields
  function validateBookForm() {
    // Get the book form inputs
    const nameInput = document.getElementById('name-book-room');
    const emailInput = document.getElementById('email-book-room');
    const dateInput = document.getElementById('date-book-room');
    const timeInput = document.getElementById('time-book-room');
    const peopleInput = document.getElementById('people-book-room');

    // Validate each field for book form
    if (nameInput.value === '') {
      alert('Please enter your name.');
      return false;
    }

    if (emailInput.value === '') {
      alert('Please enter your email.');
      return false;
    }

    if (dateInput.value === '') {
      alert('Please enter the date.');
      return false;
    }

    if (timeInput.value === '') {
      alert('Please enter the time.');
      return false;
    }

    if (peopleInput.value === '') {
      alert('Please enter the number of people.');
      return false;
    }

    return true;
  }

})();
