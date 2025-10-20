importScripts("https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.sw.js");

// Optional: Add event listeners for push notifications
self.addEventListener('push', function(event) {
    var options = {
        body: event.data.text(),
        icon: 'path/to/icon.png',
        badge: 'path/to/badge.png'
    };

    event.waitUntil(
        self.registration.showNotification('New Notification', options)
    );
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    event.waitUntil(
        clients.openWindow('https://yourwebsite.com') // Replace with your website URL
    );
});
