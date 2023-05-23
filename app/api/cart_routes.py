from flask import Blueprint, session, request, jsonify
from app.models import CartGame, Game, db
from flask_login import login_required

cart_routes = Blueprint('cart', __name__)


@cart_routes.route('/')
@login_required
def get_user_cart():
    owner_id = session.get('_user_id')
    user_cart = CartGame.query.filter_by(user_id=owner_id).all()
    # print('user_cart', user_cart)
    cart = [cart.to_dict() for cart in user_cart]
    return cart


@cart_routes.route('/', methods=['POST'])
@login_required
def add_to_cart():
    owner_id = session.get('_user_id')
    id = request.json.get('game_id')
    # print('REQUEST', request.json)
    cart_game = Game.query.get(id)
    game_in_user_cart = CartGame.query.filter(CartGame.game_id == id).filter(CartGame.user_id == owner_id).first()

    # print("DOES game EXIST IN USER CART--------------", game_in_user_cart.to_dict())

    # print ("OWNER ID--------------------", owner_id)

    if game_in_user_cart is None:
        cart_item = CartGame(user_id=owner_id, game_id=cart_game.id)
        db.session.add(cart_item)
        db.session.commit()

        return (cart_item.to_dict())

    else:
        return {'Error': 'Game already exist in cart.'}


@cart_routes.route('/deleteGame', methods=['DELETE'])
@login_required
def delete_game_from_cart():
    data = request.get_json()
    game_id = data['game_id']
    owner_id = session.get('_user_id')

    # print("DELETE ITEM FROM CART", owner_id)

    game_in_user_cart = CartGame.query.filter(CartGame.game_id == game_id).filter(CartGame.user_id == owner_id).first()

    print("DELETE game FROM CART", game_in_user_cart)

    db.session.delete(game_in_user_cart)
    db.session.commit()

    # carts = CartGame.query.filter_by(user_id=owner_id).all()
    return {'Message': "Item deleted from cart"}


@cart_routes.route('/checkoutFromCart', methods=['DELETE'])
@login_required
def checkout_from_cart():
    data = request.get_json()
    cart_owner_id = data

    all_games_in_user_cart = CartGame.query.filter(CartGame.user_id == cart_owner_id).all()

    print("DELETE ALL games FROM CART------------------------------", type(all_games_in_user_cart))
    # print("DELETE ITEM FROM CART", item_in_user_cart)

    for game in all_games_in_user_cart:
        db.session.delete(game)
        db.session.commit()

    # # carts = CartGame.query.filter_by(user_id=owner_id).all()

    return {'Message': "User's cart cleared"}
