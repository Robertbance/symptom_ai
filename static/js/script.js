/* -------------------------------------------------------------
   RÉFÉRENCES AUX ÉLÉMENTS DOM
------------------------------------------------------------- */
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const messagesDiv = document.getElementById("messages");
const darkToggle = document.getElementById("dark-toggle");

/* -------------------------------------------------------------
   CRÉATION DES BULLES DE MESSAGES
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

    return div;   // permet de supprimer la bulle (chargement)
}

/* -------------------------------------------------------------
   PROTECTION HTML (évite les injections)
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
   ENVOI DU MESSAGE UTILISATEUR AU SERVEUR (API)
------------------------------------------------------------- */
async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    // Ajout du texte utilisateur
    createBubble(text, "user");
    input.value = "";

    // Bulle de chargement
    const loadingDiv = createBubble("SymtomAI réfléchit...", "bot");

    try {
        const response = await fetch("http://127.0.0.1:5000/chatbot/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                symptome: text,
                id_user: localStorage.getItem("id_user")
            })
        });

        const data = await response.json();

        // Suppression de la bulle chargement
        if (loadingDiv) loadingDiv.remove();

        if (data.error) {
            createBubble("Erreur : " + data.error, "bot");
            return;
        }

        // Construction de la réponse diagnostique
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

        // Message automatique après diagnostic
        createBubble(
            "Avez-vous d’autres symptômes ? Je suis prêt pour vous aider à évaluer.",
            "bot"
        );

    } catch (error) {
        if (loadingDiv) loadingDiv.remove();
        createBubble("Erreur de connexion au serveur.", "bot");
    }
}

/* -------------------------------------------------------------
   ÉVÉNEMENTS BOUTON ET TOUCHE ENTRÉE
------------------------------------------------------------- */
sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keypress", e => {
    if (e.key === "Enter") sendMessage();
});

/* -------------------------------------------------------------
   MODE SOMBRE (DARK MODE)
------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", () => {
    if (!darkToggle) return;

    // Chargement de l'état précédent
    if (localStorage.getItem("darkmode") === "on") {
        document.body.classList.add("dark");
        darkToggle.textContent = "☀️";
    }

    // Toggle manuel
    darkToggle.onclick = () => {
        document.body.classList.toggle("dark");
        const isDark = document.body.classList.contains("dark");
        darkToggle.textContent = isDark ? "☀️" : "🌙";
        localStorage.setItem("darkmode", isDark ? "on" : "off");
    };
});

/* -------------------------------------------------------------
   NAVIGATION : PROFIL, HISTORIQUE, DÉCONNEXION
------------------------------------------------------------- */
const profileBtn = document.getElementById("profile-btn");
const historyBtn = document.getElementById("history-btn");
const logoutBtn = document.getElementById("logout-btn");

if (profileBtn) profileBtn.onclick = () => {
    const id = localStorage.getItem("id_user");
    window.location = id ? "/user/profile" : "/user/login";
};

if (historyBtn) historyBtn.onclick = () => {
    const id = localStorage.getItem("id_user");
    window.location = id ? "/user/history" : "/user/login";
};

if (logoutBtn) logoutBtn.onclick = () => {
    localStorage.removeItem("id_user");
    window.location = "/user/login";
};

/* -------------------------------------------------------------
   ABONNEMENT AUX NOTIFICATIONS PUSH
------------------------------------------------------------- */
async function subscribeToNotifications(userId) {
    // Demande d'autorisation au navigateur
    const permission = await Notification.requestPermission();
    if (permission !== "granted") return;

    // Enregistrement du service worker
    const registration = await navigator.serviceWorker.register("/sw.js");

    // Abonnement Web Push via VAPID
    const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: VAPID_PUBLIC_KEY
    });

    // Envoi de l'abonnement au serveur
    await fetch("/subscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            subscription,
            user_id: userId
        })
    });
}
