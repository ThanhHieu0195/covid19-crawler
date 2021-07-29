(function ($) {
  var firebaseConfig = {
    apiKey: "AIzaSyB4yFaUjh6Vab5MXA-khLWUmU_QFx0hKoU",
    authDomain: "my-project-1479109219885.firebaseapp.com",
    databaseURL: "https://my-project-1479109219885-default-rtdb.firebaseio.com",
    projectId: "my-project-1479109219885",
    storageBucket: "my-project-1479109219885.appspot.com",
    messagingSenderId: "669259492582",
    appId: "1:669259492582:web:da87d72de3a3201523df27",
    measurementId: "G-7HBFS6N0SY"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);

  const messaging = firebase.messaging();
  messaging.onMessage((payload) => {
    console.log('Message received. ', payload);
    if (payload.data['action'] == "notification" && payload.data['content'] == "NEW_UPDATE") {
      $(document).trigger("fetch_data")
    }
  });

  messaging.getToken({ vapidKey: 'BHqAJ_w3hto0kHUXj0EIZisOrFR27c0nptQi3ogjZodaq1PR04w6CJ49rE6G_lpQyYx3hzT9M44AZ4FAv11lZ48' }).then((currentToken) => {
    if (currentToken) {
      $.notify('granted permisison for notification', 'success')
      $.get('/fcm?token=' + currentToken).then(r => console.log(r))
    } else {
      $.notify('No registration token available. Request permission to generate one.', 'danger')
      console.error('No registration token available. Request permission to generate one.');
    }
  }).catch((err) => {
    console.log('An error occurred while retrieving token. error=' + err.message);
  });

  function requestPermission() {
    console.log('Requesting permission...');
    Notification.requestPermission().then((permission) => {
      if (permission === 'granted') {
        console.log('Notification permission granted.');
      } else {
        console.log('Unable to get permission to notify.', permission);
      }
    }).catch(function (error) {
      console.log(error.message)
    });
  }
})(jQuery)