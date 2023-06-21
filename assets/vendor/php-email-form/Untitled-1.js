/**
* PHP Email Form Validation - v3.6
* URL: https://bootstrapmade.com/php-email-form/
* Author: BootstrapMade.com
*/
// (function () {
// "use strict";

// let forms = document.querySelectorAll('.php-email-form');

// forms.forEach(function (e) {
//   e.addEventListener('submit', function (event) {
//     event.preventDefault();

//     let thisForm = this;

//     let action = thisForm.getAttribute('action');
//     let recaptcha = thisForm.getAttribute('data-recaptcha-site-key');

//     if (!action) {
//       displayError(thisForm, 'The form action property is not set!');
//       return;
//     }
//     thisForm.querySelector('.loading').classList.add('d-block');
//     thisForm.querySelector('.error-message').classList.remove('d-block');
//     thisForm.querySelector('.sent-message').classList.remove('d-block');

//     let formData = new FormData(thisForm);

//     if (recaptcha) {
//       if (typeof grecaptcha !== "undefined") {
//         grecaptcha.ready(function () {
//           try {
//             grecaptcha.execute(recaptcha, { action: 'php_email_form_submit' })
//               .then(token => {
//                 formData.set('recaptcha-response', token);
//                 php_email_form_submit(thisForm, action, formData);
//               })
//           } catch (error) {
//             displayError(thisForm, error);
//           }
//         });
//       } else {
//         displayError(thisForm, 'The reCaptcha javascript API url is not loaded!')
//       }
//     } else {
//       php_email_form_submit(thisForm, action, formData);
//     }
//   });
// });



//   function displayError(thisForm, error) {
//     thisForm.querySelector('.loading').classList.remove('d-block');
//     thisForm.querySelector('.error-message').innerHTML = error;
//     thisForm.querySelector('.error-message').classList.add('d-block');
//   }

// })();
// Get the form element


// Get the form elements
const contactForm = document.getElementById('contact-form');
const bookForm = document.getElementById('book-form');

// Add event listeners for form submissions
contactForm.addEventListener('submit', function (event) {
    // Prevent the form from submitting
    event.preventDefault();

    // Perform form validation for contact form
    if (validateContactForm()) {
        // If the form is valid, submit it to Formspree
        contactForm.submit();
    }
});

bookForm.addEventListener('submit', function (event) {
    // Prevent the form from submitting
    event.preventDefault();

    // Perform form validation for book form
    if (validateBookForm()) {
        // If the form is valid, submit it to Formspree
        bookForm.submit();
    }
});

// Function to validate the contact form fields
function validateContactForm() {
    // Get the contact form inputs
    const nameInput = document.getElementById('contact-name');
    const emailInput = document.getElementById('contact-email');
    const messageInput = document.getElementById('contact-message');

    // Validate each field for contact form
    if (nameInput.value === '') {
        alert('Please enter your name.');
        return false;
    }

    if (emailInput.value === '') {
        alert('Please enter your email.');
        return false;
    }

    if (messageInput.value === '') {
        alert('Please enter your message.');
        return false;
    }

    return true;
}

// Function to validate the book form fields
function validateBookForm() {
    // Get the book form inputs
    const nameInput = document.getElementById('book-name');
    const emailInput = document.getElementById('book-email');
    const dateInput = document.getElementById('book-date');
    const timeInput = document.getElementById('book-time');
    const peopleInput = document.getElementById('book-people');

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
        alert('Please enter the duration.');
        return false;
    }

    if (peopleInput.value === '') {
        alert('Please enter the number of people.');
        return false;
    }

    return true;
};
// })();