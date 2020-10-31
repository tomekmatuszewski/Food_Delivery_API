$(document).ready(function() {

    const currentLocation = location.href;
    const menu_links = document.querySelectorAll('#menu a.item');
    const menuLength = menu_links.length;
    for (let i = 0; i < menuLength; i++) {
        if (menu_links[i].href === currentLocation) {
            menu_links[i].className = "item active"
        }
    }
});