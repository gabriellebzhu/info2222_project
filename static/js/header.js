let loggedIn = window.sessionStorage.getItem("loggedIn");
let isAdmin = window.sessionStorage.getItem("isAdmin");

if (loggedIn === "True") {
    addMenuItem("/posts", "Posts");
    addMenuItem("/friends", "Friends");
    addMenuItem("/profile", "Settings");
    if (isAdmin === "True") {
        addMenuItem("/manage", "Manage");
    }
    addMenuItem("/logout", "Logout");
} else {
    addMenuItem("/login", "Login");
    addMenuItem("/join", "Join");
}

function addMenuItem(linkUrl, text) {
    var headerMenu = document.getElementById("header-menu");
    var link = document.createElement("a");
    var liItem = document.createElement("li");

    link.href = linkUrl;
    link.innerHTML = text;

    liItem.appendChild(link);
    headerMenu.appendChild(liItem);
}