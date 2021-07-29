importScripts('https://www.gstatic.com/firebasejs/8.8.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.8.0/firebase-messaging.js');
var firebaseConfig = {
  apiKey: "AIzaSyB4yFaUjh6Vab5MXA-khLWUmU_QFx0hKoU",
  authDomain: "my-project-1479109219885.firebaseapp.com",
  projectId: "my-project-1479109219885",
  storageBucket: "my-project-1479109219885.appspot.com",
  messagingSenderId: "669259492582",
  appId: "1:669259492582:web:da87d72de3a3201523df27",
  measurementId: "G-7HBFS6N0SY"
};

firebase.initializeApp(firebaseConfig);


const messaging = firebase.messaging();

messaging.onBackgroundMessage(function (payload) {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  // Customize notification here
  const notificationTitle = payload.data.title;
  const notificationOptions = {
    body: payload.data.message,
    icon: '/firebase-logo.png'
  };

  self.registration.showNotification(notificationTitle,
    notificationOptions);
});