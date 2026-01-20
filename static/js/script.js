/* -------------------------------------------------------------
   Références aux éléments DOM
------------------------------------------------------------- */
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const messagesDiv = document.getElementById("messages");
const darkToggle = document.getElementById("dark-toggle");

/* -------------------------------------------------------------
   Création des bulles de messages
------------------------------------------------------------- */
function createBubble(text, sender = "bot", html = false) {
    const div = document.createElement("div");
    div.className = `message ${sender}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    if (html) bubble.innerHTML = text;
    else bubble.textContent = text;

    div.appendChild(bubble);
    messagesDiv.appendChild(div);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    return div;
}

/* -------------------------------------------------------------
   Protection HTML
------------------------------------------------------------- */
function escapeHtml(s) {
    if (!s) return "";
    return s.replace(/[&<>"]/g, c => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;"
    })[c]);
}

/* -------------------------------------------------------------
   Envoi du message utilisateur
------------------------------------------------------------- */
async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    createBubble(text, "user");
    input.value = "";

    const loadingDiv = createBubble("SymptomAI réfléchit...", "bot");

    try {
        const response = await fetch("/chatbot/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                symptome: text,
                id_user: localStorage.getItem("id_user")
            })
        });

        if (!response.ok) {
            throw new Error("Réponse serveur invalide");
        }

        const data = await response.json();
        loadingDiv.remove();

        if (data.error) {
            createBubble("Erreur : " + data.error, "bot");
            return;
        }

        const diagnosisHTML = `
            <div><strong>Diagnostic possible :</strong> ${escapeHtml(data.maladie_predite)}</div>

            <div class="diagnosis-card">
                <div class="diagnosis-title">${escapeHtml(data.maladie_predite)}</div>

                <div>
                    <strong>Symptôme similaire :</strong>
                    <span class="symptom-tag">${escapeHtml(data.exemple_symptome)}</span>
                </div>

                <div>
                    <strong>Confiance :</strong>
                    ${(data.similarite_max * 100).toFixed(1)} %
                </div>

                <div class="confidence-bar">
                    <div class="confidence-fill" style="width:${data.similarite_max * 100}%"></div>
                </div>

                <p style="margin-top:10px;">
                    <strong>Recommandation :</strong><br>
                    ${escapeHtml(data.diagnostic_reference)}
                </p>
            </div>
        `;

        createBubble(diagnosisHTML, "bot", true);
        createBubble(
            "Avez-vous d’autres symptômes ? Je suis prêt pour vous aider à évaluer.",
            "bot"
        );

    } catch (error) {
        if (loadingDiv) loadingDiv.remove();
        createBubble("Erreur de connexion au serveur.", "bot");
        console.error(error);
    }
}

/* -------------------------------------------------------------
   Événements
------------------------------------------------------------- */
sendBtn.addEventListener("click", sendMessage);

input.addEventListener("keypress", e => {
    if (e.key === "Enter") sendMessage();
});

/* -------------------------------------------------------------
   Mode sombre
------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", () => {
    if (!darkToggle) return;

    if (localStorage.getItem("darkmode") === "on") {
        document.body.classList.add("dark");
        darkToggle.textContent = "☀️";
    }

    darkToggle.onclick = () => {
        document.body.classList.toggle("dark");
        const isDark = document.body.classList.contains("dark");
        darkToggle.textContent = isDark ? "☀️" : "🌙";
        localStorage.setItem("darkmode", isDark ? "on" : "off");
    };
});

/* -------------------------------------------------------------
   Navigation
------------------------------------------------------------- */
const profileBtn = document.getElementById("profile-btn");
const historyBtn = document.getElementById("history-btn");
const logoutBtn = document.getElementById("logout-btn");

if (profileBtn) profileBtn.onclick = () => {
    const id = localStorage.getItem("id_user");
    window.location = id ? "/user/profile" : "/login";
};

if (historyBtn) historyBtn.onclick = () => {
    const id = localStorage.getItem("id_user");
    window.location = id ? "/user/history" : "/login";
};

if (logoutBtn) logoutBtn.onclick = () => {
    localStorage.removeItem("id_user");
    window.location = "/login";
};
