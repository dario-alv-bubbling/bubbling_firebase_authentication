const express = require('express')
const app = express()
const port = 3000

const firebase = require('firebase/app');
// Add the Firebase products that you want to use
require("firebase/auth");

var bodyParser = require('body-parser');
app.use(bodyParser.json()); // support json encoded bodies

app.get('/', (req, res) => {
    res.send('Hello World!')
})

app.post('/login', function (req, res) {
    var email = req.body.email
    var password = req.body.password


    firebase.auth().signInWithEmailAndPassword(email, password)
        .then((user) => {
            console.log('logged in with email/pass')
            res.send(user);
        })
        .catch((error) => {
            var errorCode = error.code;
            var errorMessage = error.message;
            console.log(errorMessage)
            res.send(errorCode + ' ' + errorMessage);

        });
})

app.post('/login-with-token', function (req, res) {
    var token = req.body.token

    firebase.auth().signInWithCustomToken(token)
        .then((user) => {
            console.log('logged in with custom token')
            res.send(user);
        })
        .catch((error) => {
            var errorCode = error.code;
            var errorMessage = error.message;
            console.log(errorMessage)
            res.send(errorCode + ' ' + errorMessage);

        });
})

app.listen(port, () => {

    console.log(`Example app listening at http://localhost:${port}`)

    // Your web app's Firebase configuration
    // For Firebase JS SDK v7.20.0 and later, measurementId is optional
    var firebaseConfig = {
        apiKey: "AIzaSyAtSACx_m_ul_dcsxtLaMLZ3aEukIiEhI4",
        authDomain: "bubbling-project.firebaseapp.com",
        databaseURL: "https://bubbling-project.firebaseio.com",
        projectId: "bubbling-project",
        storageBucket: "bubbling-project.appspot.com",
        messagingSenderId: "573107455749",
        appId: "1:573107455749:web:ce8c5bf6bb2e296f27996c",
        measurementId: "G-SEKN6Q8Y0H"
    };
    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);
})