var lang = "en"; // Default language is English

// Load the translations file
fetch("translations.json")
    .then(response => response.json())
    .then(data => {
        var translations = data;

        // Update text on the page using translations
        document.querySelector("#welcome-text").textContent = translations[lang].welcome_message;
        document.querySelector("#welcome").textContent = translations[lang].welcome;
        document.querySelector("#link-about").textContent = translations[lang].about;
        document.querySelector("#link-contact").textContent = translations[lang].contact;
        document.querySelector("header nav ul li:nth-child(1) a").textContent = translations[lang].about;
        document.querySelector("header nav ul li:nth-child(2) a").textContent = translations[lang].contact;
        document.querySelector("main section#about h2").textContent = translations[lang].about;
        document.querySelector("main section#about p").textContent = translations[lang].about_text;
        document.querySelector("main section#contact h2").textContent = translations[lang].contact;
        document.querySelector("main section#contact form label[for='name']").textContent = translations[lang].name;
        document.querySelector("main section#contact form label[for='email']").textContent = translations[lang].email;
        document.querySelector("main section#contact form label[for='message']").textContent = translations[lang].message;
        document.querySelector("main section#contact form button[type='submit']").textContent = translations[lang].submit;
        document.querySelector("footer p").textContent = translations[lang].footer;
    })
    .catch(error => {
        console.error("Error loading translations file:", error);
    });
