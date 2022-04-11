var forge = require('node-forge');

var key = forge.random.getBytesSync(16);
var iv = forge.random.getBytesSync(16);

let friend_pem = window.friend_pk;
let friend_pk = forge.pki.publicKeyFromPem(friend_pem);


function send_secret(key, iv, friend_pk) {
    key_and_iv = friend_pk.encrypt(key + iv);
    $.ajax({
        type: "POST",
        url: window.location.href,
        contentType: "application/json",
        data: JSON.stringify({message: message}),
        dataType: "json",
        success: disp_msg
    });
}
