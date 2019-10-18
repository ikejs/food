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
title = " | Food"


# users = db.users
# restaurants = db.restaurants
# menus = db.menus
# orders = db.orders


# users = [
#     {
#         "_id": "fakeUserId1234567",
#         "name": "Ike Holzmann",
#         "email": "ikeholzmann@gmail.com",
#         "phone": "19202519700",
#         "addresses": [],
#         "type": "seller"
#     },
#     {
#         "_id": "fakeUserId7654321",
#         "name": "Bill Smith",
#         "email": "bill@smith.com",
#         "phone": "19202519696",
#         "addresses": [
#             { "street": "851 California St", "city": "San Francisco", "state": "CA", "zip": "94108" },
#             { "street": "26 Glenwood Ct", "city": "Fond du Lac", "state": "WI", "zip": "54935" }
#         ],
#         "type": "buyer"
#     }
# ]
#
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
#
# menus = [
#     {
#         "_id": "fakeMenuId1234567",
#         "name": "Lunch Menu",
#         "categories": [
#             { "_id": "fakeCategoryId1", "name": "Burgers" },
#             { "_id": "fakeCategoryId2", "name": "Fries" },
#             { "_id": "fakeCategoryId3", "name": "Shakes" },
#             { "_id": "fakeCategoryId4", "name": "Desserts" }
#         ],
#         "items": [
#             {
#                 "categories": ["fakeCategoryId1"],
#                 "name": "Big Ol Burger",
#                 "description": "This burger is really big, bro.",
#                 "price": 8.95,
#                 "image": "https://assets.bonappetit.com/photos/5d1cb1880813410008e914fc/16:9/w_1200,c_limit/Print-Summer-Smash-Burger.jpg",
#                 "modifiers": [],
#                 "variations": [],
#                 "addons": [
#                     { "name": "Add Cheese", "price": 1.99 },
#                     { "name": "Add Onions", "price": 0.99 }
#                 ]
#             },
#             {
#                 "categories": ["fakeCategoryId1"],
#                 "name": "Lil Burger",
#                 "description": "This burger is really pretty small, bro.",
#                 "price": 4.95,
#                 "image": "https://media.istockphoto.com/photos/small-burger-picture-id660640390",
#                 "modifiers": [],
#                 "variations": [],
#                 "addons": [
#                     { "name": "Add Cheese", "price": 0.99 },
#                     { "name": "Add Onions", "price": 0.40 }
#                 ]
#             },
#             {
#                 "categories": ["fakeCategoryId2"],
#                 "name": "Fries",
#                 "description": "These are some sweet potato fries.",
#                 "price": 3.99,
#                 "image": "https://www.iheartnaptime.net/wp-content/uploads/2018/05/sweet-potato-fries.jpg",
#                 "modifiers": [],
#                 "variations": [
#                     { "name": "Regular", "price": 0.00 },
#                     { "name": "Sweet Potato", "price": 0.00 }
#                 ],
#                 "addons": [
#                     { "name": "Add Ketchup", "price": 0.99 }
#                 ]
#             },
#             {
#                 "categories": ["fakeCategoryId3", "fakeCategoryId4"],
#                 "name": "Famous Shake",
#                 "description": "This is a really good shake.",
#                 "price": 0,
#                 "image": "https://media2.s-nbcnews.com/i/newscms/2017_20/1214849/shake-shack-chocolate-shake-today-170510-tease_05e84fb9d50c206919acf687070b7a09.jpg",
#                 "modifiers": [
#                     { "name": "Small", "price": 3.99 },
#                     { "name": "Medium", "price": 4.99 },
#                     { "name": "Large", "price": 5.99 }
#                 ],
#                 "variations": [
#                     { "name": "Vanilla", "price": 0.00 },
#                     { "name": "Chocolate", "price": 0.00 },
#                     { "name": "Strawberry", "price": 0.30 }
#                 ],
#                 "addons": []
#             }
#         ]
#     }
# ]


# CRUD MENU
@app.route("/account/menus")
def account_view_menus():
    return render_template(
    'account/menus.html',
    restaurant = restaurants[0],
    menus = menus.find()
    )

@app.route("/account/menus", methods=['POST'])
def account_add_menu():
    menus.insert_one({ 'label': request.form.get('menuName') })
    flash(b'Menu added successfully.', 'success')
    return redirect(url_for('account_view_menus'))

@app.route("/account/menu/create")
def account_create_category_form():
    return render_template(
    'account/category_create.html',
    title = 'Create Category' + title,
    restaurant = restaurants[0],
    menu = {}
    )

@app.route("/account/menu/create", methods=['POST'])
def account_create_menu():
    menu = {
        "name": request.form.get('name'),
        "categories": [],
        "items": []
    }
    menus.append(menu)
    return redirect(url_for('account_view_menus', menu=menus[0]))

@app.route("/account/menu/<menu_id>")
def account_get_menu(menu_id):
    menu = menus.find_one({ '_id': ObjectId(menu_id) })
    return render_template(
    'account/menu_edit.html',
    title = 'Edit ' + menu['label'] + title,
    restaurant = restaurants[0],
    menu = menu
    )

@app.route("/account/menu/<menu_id>", methods=['POST'])
def account_edit_menu(menu_id):
    menus.update_one(
        {'_id': ObjectId(menu_id)},
        {'$set': { 'label': request.form.get('label') } }
        )
    flash(u'Menu saved successfully.', 'success')
    return redirect(url_for('account_get_menu',
    menu_id = menu_id
    )
    )

@app.route("/account/menus/delete", methods=['POST'])
def account_delete_menu():
    menus.delete_one({'_id': ObjectId(request.form.get('menuId')) })
    flash(u'Menu deleted successfully.', 'info')
    return redirect(url_for('account_view_menus'))





if __name__ == "__main__":
    app.run()
