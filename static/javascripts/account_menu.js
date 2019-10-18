function saveMenu() {
    let changes = null;
    $.post(window.location.pathname, changes).done(function(data) {
        location.reload();
    });
}
