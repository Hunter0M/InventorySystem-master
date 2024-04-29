
import translations from "./translations.js";   // translations = object of translations

// Here start code for traslations  

const languageSelector = document.querySelector("select");   // select = select tag
languageSelector.addEventListener("change", (event) => {    
  setLanguage(event.target.value);   // setLanguage = function to set the language
  localStorage.setItem("lang", event.target.value); 
});

document.addEventListener("DOMContentLoaded", () => {  //# = id , . = class , [data-i18n] = attribute
  const language = localStorage.getItem("lang") || "en";     // اذا لم تكن اللغة متوفرة استخدم الانجليزية
  setLanguage(language);    
});

const setLanguage = (language) => {   // setLanguage = function to set the language
  const elements = document.querySelectorAll("[data-i18n]");    //# = id , . = class , [data-i18n] = attribute
  elements.forEach((element) => {   // forEach = for each element in the array
    const translationKey = element.getAttribute("data-i18n");   // data-i18n = key of the translation
    element.textContent = translations[language][translationKey];   // textContent = text inside the element
  });
  document.dir = language === "ar" ? "rtl" : "ltr"; // ltr = left to right , rtl = right to left , 
};
// Here end code for traslations