function saveMenu() {
    let changes = null;
    $.post(window.location.pathname, changes).done(function(data) {
        location.reload();
    });
}

function deleteMenu(menuId) {
    if (confirm('Are you sure you want to delete this menu?')) {
        if (confirm('It will be permanently erased. This action is irreversible.')) {
            $("#deleteMenuForm").submit();
        }
    }
    return false;
}
