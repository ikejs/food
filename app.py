from flask import Flask, flash, render_template, flash, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
import json
load_dotenv()

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/food')
client = MongoClient(host=host)
db = client.get_default_database()
menus = db['menus']


app = Flask(__name__, static_url_path='')
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
title = " | Food" # Dynamic titles


# Test restaurant without auth
restaurants = [
    {
        "_id": "fakeRestaurantId1234567",
        "name": "Ike's Burgers",
        "slug": "ikes-burgers",
        "menus": ["fakeMenuId1234567"],
        "delivery": True,
        "takeout": False,
        "sellers": ["fakeUserId1234567"]
    }
]



@app.route("/account/menus")
def account_view_menus():
    '''
    Add new menu from backdoor, return to menus view
    '''
    return render_template(
    'account/menus.html',
    restaurant = restaurants[0],
    menus = menus.find()
    )

@app.route("/account/menus", methods=['POST'])
def account_add_menu():
    '''
    Add new menu from backdoor, return to menus view
    '''
    menus.insert_one({ 'label': request.form.get('menuName'), 'description': request.form.get('menuDescription'), 'categories': [] })
    flash(b'Menu added successfully.', 'success')
    return redirect(url_for('account_view_menus'))

@app.route("/account/menus/newCategory", methods=['POST'])
def account_add_category():
    '''
    Add mew category from backdoor, redirect to the menu that holds the category.
    '''
    menuId = request.form.get('menuId')
    newCategoryLabel = request.form.get('categoryName')
    newCategoryDescription = request.form.get('categoryDescription')
    menus.update(
       { '_id': ObjectId(menuId) },
       { '$push': { 'categories': { '_id': ObjectId(), 'label': newCategoryLabel, 'description': newCategoryDescription, 'items': [] } } }
    )
    flash(b'Category added successfully.', 'success')
    return redirect(url_for('account_get_menu', menu_id=menuId))


@app.route("/account/menus/newItem", methods=['POST'])
def account_add_item():
    '''
    Add new item from backdoor, return to menu that holds item
    '''
    print(request.form) # VIEW PRINT RESPONSE, STORE ITEM OPTIONS CORRECTLY...
    menuId = request.form.get('menuId')
    categoryId = request.form.get('categoryId')
    label = request.form.get('newItemName')
    description = request.form.get('newItemDescription')

    menus.update(
       { '_id': ObjectId(menuId), 'categories._id': ObjectId(categoryId) },
       { '$push': { 'categories.$.items': { '_id': ObjectId(), 'label': label, 'description': description, 'options': [] } } }
    )
    flash(b'Item added successfully.', 'success')
    return redirect(url_for('account_get_menu', menu_id=menuId))


@app.route("/account/menu/<menu_id>")
def account_get_menu(menu_id):
    '''
    Add new menu from backdoor, return to menus view
    '''
    menu = menus.find_one({ '_id': ObjectId(menu_id) })
    return render_template(
    'account/menu_edit.html',
    title = 'Edit ' + menu['label'] + title,
    restaurant = restaurants[0],
    menu = menu
    )

@app.route("/account/menu/<menu_id>", methods=['POST'])
def account_edit_menu(menu_id):
    '''
    Update menu details from backdoor, return to menu page
    '''
    menu = menus.find_one({ '_id': ObjectId(menu_id) })
    updatedCategories = []
    for category in menu['categories']:
        updatedCategories.append({
        '_id': ObjectId(category['_id']),
        'label': request.form.get('categoryLabel_'+str(category['_id'])),
        'description': request.form.get('categoryDescription_'+str(category['_id'])),
        'items': []
        })
    updatedMenu = {
        'label': request.form.get('menuLabel'),
        'description': request.form.get('menuDescription'),
        'categories': updatedCategories
    }
    menus.update_one(
        {'_id': ObjectId(menu_id)},
        {'$set': updatedMenu }
        )
    flash(u'Menu saved successfully.', 'success')
    return redirect(url_for('account_get_menu',
    menu_id = menu_id
    )
    )

@app.route("/account/menus/delete", methods=['POST'])
def account_delete_menu():
    '''
    Delete menu from backdoor, return to menus view
    '''
    menus.delete_one({'_id': ObjectId(request.form.get('menuId')) })
    flash(u'Menu deleted successfully.', 'info')
    return redirect(url_for('account_view_menus'))


@app.route("/account/menus/deleteCategory", methods=['POST'])
def account_delete_category():
    '''
    Delete menu category from backdoor, return to the menu page it belonged to
    '''
    menus.update_one(
        {'_id': ObjectId(request.form.get('menuId'))},
        { '$pull': { "categories" : { '_id': ObjectId(request.form.get('categoryId')) } } }, False, True
    );
    flash(u'Category deleted successfully.', 'info')
    return redirect(url_for('account_get_menu',
    menu_id = request.form.get('menuId')
    )
    )



@app.route("/account/getObjectId", methods=['POST'])
def generate_objectId():
    '''
    Send ObjectIds to client for creating menu item modifiers
    '''
    object = ObjectId()
    return str(object)



if __name__ == "__main__":
    app.run()
