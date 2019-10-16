from flask import Flask
app = Flask(__name__)




# CRUD MENU
@app.route("/account/menu/create")
def account_create_menu_form():
    return "GET CREATE MENU FORM"

@app.route("/account/menu/create", methods=['POST'])
def account_create_menu():
    return "POST NEW MENU"

@app.route("/account/menu/<menu_id>")
def account_view_menu(menu_id):
    return "View/Edit Menu "+menu_id

@app.route("/account/menu/<menu_id>", methods=['PUT'])
def account_edit_menu(menu_id):
    return "PUT menu "+menu_id

@app.route("/account/menu/<menu_id>", methods=['DELETE'])
def account_delete_menu(menu_id):
    return "DELETE menu "+menu_id

# CRUD ITEM
@app.route("/account/item/create")
def account_create_item_form():
    return "GET CREATE ITEM FORM"

@app.route("/account/item/create", methods=['POST'])
def account_create_item():
    return "POST NEW ITEM"

@app.route("/account/item/<item_id>")
def account_view_item(item_id):
    return "View/Edit Item "+item_id

@app.route("/account/item/<item_id>", methods=['PUT'])
def account_edit_item(item_id):
    return "PUT Item "+item_id

@app.route("/account/item/<item_id>", methods=['DELETE'])
def account_delete_item(item_id):
    return "DELETE Item "+item_id




if __name__ == "__main__":
    app.run()
