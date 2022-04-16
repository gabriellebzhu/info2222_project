var forge = require('node-forge');

var key = forge.random.getBytesSync(16);
var iv = forge.random.getBytesSync(16);

let friend_pem = window.friend_pk;
let friend_pk = forge.pki.publicKeyFromPem(friend_pem);


function get_secret(key, iv, friend_pk) {
    console.log(window.old_chat_len);
    let key_and_iv = "none";
    if (window.old_chat_len === "0") {
        key_and_iv = friend_pk.encrypt(key + iv);
    }
    return key_and_iv
}

// function getCookie(cookie_name) {
//     // from W3Schools
//     let name = cookie_name + "=";
//     let decodedCookie = decodeURIComponent(document.cookie);
//     let ca = decodedCookie.split(';');
//     for(let i = 0; i <ca.length; i++) {
//         let c = ca[i];
//         while (c.charAt(0) == ' ') {
//             c = c.substring(1);
//         }
//         if (c.indexOf(name) == 0) {
//             return c.substring(name.length, c.length);
//         }
//     }
//     return "";
// }

function sym_encrypt(message) {
    var cipher = forge.cipher.createCipher('AES-CBC', key);
    cipher.start({iv: iv});
    cipher.update(forge.util.createBuffer(message));
    cipher.finish();
    return cipher.output.toString('binary');
}


function send_msg(message) {
    // encrypt message with pub key of friend
    console.log("msg: " + message);
    enc_message = sym_encrypt(message);
    console.log("encrypted msg: " + sym_encrypt(enc_message));

    enc_secret = get_secret(key, iv, friend_pk);
    $.ajax({
        type: "POST",
        url: window.location.href,
        contentType: "application/json",
        data: JSON.stringify({secret: enc_secret, message: enc_message}),
        dataType: "json",
        success: disp_msg
    });
};

var form = document.getElementById('message-form');
form.addEventListener("submit", function (event) {
    event.preventDefault();
    let msg = document.getElementById("msg-input").value;
    console.log(msg)
    send_msg(msg);
});

//     let username = getCookie('account');

var disp_msg = function(response) {
    var ul = document.getElementById("message-list");
    var li = document.createElement("li");
    msg = document.getElementById("msg-input").value;
    li.appendChild(document.createTextNode(response.username + ": " + msg));
    ul.appendChild(li);
    let len = document.getElementById('message-list').getElementsByTagName('li').length
    form.reset();
    while (len > 10) {
        ul.removeChild(ul.childNodes[0]);
        len--;
        console.log("curr_len: " + len);
    }
};
