
// Load translations from JSON file
function loadTranslations() {
    return fetch('Users/julienhubar/Documents/lvdpdc/assets/js/translations.json')
        .then(response => response.json())
        .then(data => data);
}

// Initialize i18next
function initI18next(translations) {
    i18next.init({
        lng: 'en', // Default language
        fallbackLng: 'en', // Fallback language
        resources: translations
    });
}

// Function to translate text
function translateText() {
    // Translate menu label
    let menuLabelElement = document.querySelector('.scrollto');
    if (menuLabelElement) {
        menuLabelElement.textContent = i18next.t('menuLabel');
    }

    // Translate page title
    let pageTitleElement = document.querySelector('title');
    if (pageTitleElement) {
        pageTitleElement.textContent = i18next.t('pageTitle');
    }


}

// Language switcher event listener
function changeLanguage(language) {
    i18next.changeLanguage(language, (err, t) => {
        if (err) return console.error(err);
        translateText(); // Call the function to translate text on language change
    });
}

// Load translations and initialize i18next
loadTranslations()
    .then(translations => {
        initI18next(translations);
        translateText(); // Call the function to translate the initial text
    });
