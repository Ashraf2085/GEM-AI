document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('input'); // ton champ texte
    const button = document.querySelector('.search-button'); // ton bouton
    const chatContainer = document.getElementById('chat-messages'); // div du chat

    // Fonction pour envoyer un message
    function envoyerMessage() {
        const userText = input.value.trim().toLowerCase();
        if (!userText) return;

        chatContainer.innerHTML += `<div class="message-user">Toi : ${userText}</div>`;

        fetch(`/get_response?question=${encodeURIComponent(userText)}`)
            .then(response => response.text())
            .then(data => {
                chatContainer.innerHTML += `<div class="message-bot">AI : ${data}</div>`;
                chatContainer.scrollTop = chatContainer.scrollHeight;
            });

        input.value = '';
    }

    // Clic sur le bouton
    button.addEventListener('click', envoyerMessage);

    // Touche Enter dans le champ input
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault(); // empêche le saut de ligne
            envoyerMessage();
        }
    });

    // Le reste de ton code (sidebar, overlay, etc.) reste identique
});

// On cible les éléments avec les bons IDs et classes de TON HTML
const toggleBtn = document.getElementById('toggle-menu-btn');
const sidebar = document.querySelector('.sidebar');
const mainContent = document.querySelector('.main-content');

// On écoute le clic sur le bouton
toggleBtn.addEventListener('click', () => {
    // On ajoute/enlève la classe 'open' sur la sidebar
    sidebar.classList.toggle('open');
    // On ajoute/enlève la classe 'shifted' sur le contenu principal
    mainContent.classList.toggle('shifted');
});

// Fermer le menu si on clique sur l'overlay
overlay.addEventListener('click', () => {
    sidebar.classList.remove('open');
    overlay.classList.remove('active');
    toggleBtn.textContent = '☰';
});

function changerMode(mode) {
    fetch("http://127.0.0.1:8001/set_mode", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ mode: mode })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Mode changé :", data.mode);
    })
    .catch(error => console.error("Erreur :", error));
}
