const themeToggleButton = document.getElementById("theme-toggle");
const body = document.body;

// Vérification de la préférence du thème dans le localStorage
const savedTheme = localStorage.getItem("theme");

if (savedTheme === "dark") {
    body.classList.add("dark-mode");
    themeToggleButton.textContent = "Enable RGB Mode"; // Affiche "Enable RGB Mode"
} else if (savedTheme === "rgb") {
    body.classList.add("rgb-mode");
    themeToggleButton.textContent = "Disable RGB Mode"; // Affiche "Disable RGB Mode"
} else {
    // Mode par défaut : light mode
    localStorage.setItem("theme", "light");
    themeToggleButton.textContent = "Enable RGB Mode";
}

// Événement de bascule entre les modes
themeToggleButton.addEventListener("click", () => {
    if (body.classList.contains("dark-mode")) {
        // Passe en mode RGB
        body.classList.remove("dark-mode");
        body.classList.add("rgb-mode");
        themeToggleButton.textContent = "Disable RGB Mode";
        localStorage.setItem("theme", "rgb");
    } else if (body.classList.contains("rgb-mode")) {
        // Retourne au mode sombre (Night Mode)
        body.classList.remove("rgb-mode");
        body.classList.add("dark-mode");
        themeToggleButton.textContent = "Enable RGB Mode";
        localStorage.setItem("theme", "dark");
    } else {
        // Retour au mode par défaut (light mode)
        body.classList.add("dark-mode");
        themeToggleButton.textContent = "Enable RGB Mode";
        localStorage.setItem("theme", "dark");
    }
});
