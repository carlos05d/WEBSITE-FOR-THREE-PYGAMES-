const themeToggleButton = document.getElementById("theme-toggle");
const body = document.body;

// Check local storage for theme preference
if (localStorage.getItem("theme") === "dark") {
    body.classList.add("dark-mode");
    themeToggleButton.textContent = "White Mode";
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
