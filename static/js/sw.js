// Service Worker - Réception des notifications Push

self.addEventListener("push", event => {
    const data = event.data.json();

    // Icône en Base64 (aucun fichier image nécessaire)
    const base64Icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAQAAAAAYLlVAAAAyklEQVR4Ae3Y0Q3CMBAG4L+nxgGkEjpJG5BCkoZtKChpGo7AGfG5uXdzbp0u03Pf+w3z04AAAAAAADgJr2DN2kcikJsGwqgicOgU4nAQrE9JyA5qsBGuo9TcACKJyxqSCeS8inGdJf6d2u0K1tqGkZ2QHCtAoqmB/0gFQM0FQG2pBnqgZJo5jMrSPOXYicOIUSsAp5BFej6cAH8F0ouxkFeS29oGhh7gE7AF7kJPgVtGv7MZwSQAAAAASUVORK5CYII=";

    event.waitUntil(
        self.registration.showNotification(data.title, {
            body: data.message,
            icon: base64Icon,
            badge: base64Icon
        })
    );
});
