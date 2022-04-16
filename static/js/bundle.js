(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
// var forge = require('node-forge');
// var pk;

// var pk = function(){
//     pk = forge.pki.publicKeyFromPem(data);
//     return pk;
// }


// window.onload=function(){
//     pk()
// };

// var form = document.getElementById('login-form');
// form.addEventListener("submit", function (event) {
//     event.preventDefault();

//     var pass = form.elements['password']
//     var user = form.elements['username']

//     if (pass == '') {
//         console.log("AAAHH");
//     } else if (user == '') {
//         console.log("AAAHH");
//     }

//     pass = pk.encrypt(pass)
//     console.log(pass)
//     document.getElementById('password').value = pass

//     user = pk.encrypt(user)
//     console.log(pass)
//     document.getElementById('username').value = user

//     form.submit()
// });



// document.getElementById("testing").innerHTML = keys.privateKey;
},{}]},{},[1]);
