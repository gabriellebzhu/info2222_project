var forge = require('node-forge');

var form = document.getElementById('login-form');
form.addEventListener("submit", function (event) {
    event.preventDefault();

    var pass = document.getElementById("password").value;
    var user = document.getElementById("username").value;

    if (pass == '') {
        document.getElementById('login-validity').innerHTML = 'Please enter a password';
        console.log("AAAHH");
        return;
    } else if (user == '') {
        document.getElementById('login-validity').innerHTML = 'Please enter a username';
        console.log("AAAHH");
        return;
    }

    let user_pk = gen_keys;
    console.log("cookies: " + document.cookie)

    $.ajax({
        type: "POST",
        url: "/login",
        contentType: "application/json",
        data: JSON.stringify({user_pk: user_pk, username: user, password: pass}),
        dataType: "json",
        success: parse_response
    });
});

var parse_response = function(response) {
    console.log(response.message);
    if (response.success === '1') {
        window.location.replace("/friends");
    } else {
        document.getElementById('login-validity').innerHTML = 'Username and password combination are incorrect';
    }

}

var gen_keys = function() {
    let keys = forge.pki.rsa.generateKeyPair(2048);
    document.cookie = "private_key=" + keys.privateKey;
    return keys.publicKey;
}

// $(document).ready(function() {
//     // if (window.isRegister === 'false') {
//         $.ajax({
//             type: "POST",
//             url: "_get_user_pk_json",
//             contentType: "application/json",
//             data: JSON.stringify({user_pk: "TESTING!!!"}),
//             dataType: "json"
//         });
//     // }
// });


// window.onload=function(){
//     // if (isRegister === 'false') {
//         // var keys = forge.pki.rsa.generateKeyPair(2048);

//         // document.cookie = "private_key=" + keys.privateKey;
//         // var user_pk = keys.publicKey;

//         $.ajax({
//             type: "POST",
//             url: "_get_user_pk_json",
//             contentType: "application/json",
//             data: JSON.stringify({user_pk: "TESTING!!!"}),
//             dataType: "json",
//         });
//     // }
// };