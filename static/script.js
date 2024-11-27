const themeToggleButton = document.getElementById("theme-toggle");
const body = document.body;

// Check local storage for theme preference
const savedTheme = localStorage.getItem("theme");
if (savedTheme === "dark") {
    body.classList.add("dark-mode");
    themeToggleButton.textContent = "White Mode";
} else if (savedTheme === "light") {
    body.classList.remove("dark-mode");
    themeToggleButton.textContent = "Night Mode";
} else {
    // Default to light theme if no preference is saved
    localStorage.setItem("theme", "light");
    themeToggleButton.textContent = "Night Mode";
}

// Toggle between light and dark mode
themeToggleButton.addEventListener("click", () => {
    body.classList.toggle("dark-mode");

    if (body.classList.contains("dark-mode")) {
        themeToggleButton.textContent = "White Mode";
        localStorage.setItem("theme", "dark");
    } else {
        themeToggleButton.textContent = "Night Mode";
        localStorage.setItem("theme", "light");
    }
});
