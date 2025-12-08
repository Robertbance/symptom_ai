// Gestion du mode sombre (Dark Mode)
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("dark-toggle");
    if (!toggle) return;

    // Charger préférence
    if (localStorage.getItem("darkmode") === "on") {
        document.body.classList.add("dark");
        toggle.textContent = "☀️";
    }

    toggle.onclick = () => {
        document.body.classList.toggle("dark");

        if (document.body.classList.contains("dark")) {
            toggle.textContent = "☀️";
            localStorage.setItem("darkmode", "on");
        } else {
            toggle.textContent = "🌙";
            localStorage.setItem("darkmode", "off");
        }
    };
});
