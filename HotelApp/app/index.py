import json

from flask import Flask
import math
from flask import render_template, request, redirect, jsonify, session
from sqlalchemy.orm.util import eval_name_only

from HotelApp.app import app, login
import dao
from flask_login import login_user, logout_user, current_user

@app.route('/')
def homePage():
    # dao.add_config_parameters(28, 100)
    #
    # dao.add_room_type("Standard Room", 10, 10, 1)
    # dao.add_room_type("Deluxe Room", 20, 10, 1)
    # dao.add_room_type("Suite", 30, 10, 1)
    #
    # dao.add_room("Single Room", "A Single Room in a hotel is designed to accommodate one guest, making it ideal for solo travelers or business guests. The room typically features a single bed (twin size) or sometimes a small double bed, depending on the hotel's standard. The average room size is around 15-20 square meters, providing a compact yet comfortable space.", "A Single Room accommodates 1 guest with a single bed, ideal for solo travelers, offering basic amenities.", 10, 1, 4,4, True, 1)
    # dao.add_room("Double Room", "A Double Room in a hotel is designed to accommodate two guests comfortably. It typically features one double bed or sometimes a queen-size bed, making it ideal for couples or travelers who prefer to share a bed. The room size is usually around 20-25 square meters, providing enough space for relaxation.", "A Double Room accommodates 2 guests with one double or queen-size bed, ideal for couples or friends.", 20,2,3,3, True, 1)
    # dao.add_room("Triple Room", "A Triple Room in a hotel is designed to accommodate three guests comfortably. It typically features either one double bed and one single bed or three single beds, depending on the hotel's layout. The room is spacious, usually ranging from 25 to 35 square meters, and comes equipped with essential amenities such as a private bathroom, air conditioning, a flat-screen TV, free Wi-Fi, a minibar, and tea/coffee-making facilities.", "A Triple Room accommodates 3 guests with 1 double and 1 single bed or 3 single beds, ideal for families or friends.", 30, 3,3, 3,True, 1)
    #
    # dao.add_room("Single Room", "A Single Room in a hotel is designed to accommodate one guest, making it ideal for solo travelers or business guests. The room typically features a single bed (twin size) or sometimes a small double bed, depending on the hotel's standard. The average room size is around 15-20 square meters, providing a compact yet comfortable space.", "A Single Room accommodates 1 guest with a single bed, ideal for solo travelers, offering basic amenities.", 10,1,4,4, True, 2)
    # dao.add_room("Double Room", "A Double Room in a hotel is designed to accommodate two guests comfortably. It typically features one double bed or sometimes a queen-size bed, making it ideal for couples or travelers who prefer to share a bed. The room size is usually around 20-25 square meters, providing enough space for relaxation.", "A Double Room accommodates 2 guests with one double or queen-size bed, ideal for couples or friends.", 20, 2,3,3, True, 2)
    # dao.add_room("Triple Room", "A Triple Room in a hotel is designed to accommodate three guests comfortably. It typically features either one double bed and one single bed or three single beds, depending on the hotel's layout. The room is spacious, usually ranging from 25 to 35 square meters, and comes equipped with essential amenities such as a private bathroom, air conditioning, a flat-screen TV, free Wi-Fi, a minibar, and tea/coffee-making facilities.", "A Triple Room accommodates 3 guests with 1 double and 1 single bed or 3 single beds, ideal for families or friends.", 30,3,3, 3,True, 2)
    #
    # dao.add_room("Single Room", "A Single Room in a hotel is designed to accommodate one guest, making it ideal for solo travelers or business guests. The room typically features a single bed (twin size) or sometimes a small double bed, depending on the hotel's standard. The average room size is around 15-20 square meters, providing a compact yet comfortable space.", "A Single Room accommodates 1 guest with a single bed, ideal for solo travelers, offering basic amenities.", 10, 1,4,4, True, 3)
    # dao.add_room("Double Room", "A Double Room in a hotel is designed to accommodate two guests comfortably. It typically features one double bed or sometimes a queen-size bed, making it ideal for couples or travelers who prefer to share a bed. The room size is usually around 20-25 square meters, providing enough space for relaxation.", "A Double Room accommodates 2 guests with one double or queen-size bed, ideal for couples or friends.", 20,2,3,3, True, 3)
    # dao.add_room("Triple Room", "A Triple Room in a hotel is designed to accommodate three guests comfortably. It typically features either one double bed and one single bed or three single beds, depending on the hotel's layout. The room is spacious, usually ranging from 25 to 35 square meters, and comes equipped with essential amenities such as a private bathroom, air conditioning, a flat-screen TV, free Wi-Fi, a minibar, and tea/coffee-making facilities.", "A Triple Room accommodates 3 guests with 1 double and 1 single bed or 3 single beds, ideal for families or friends.", 30,3,3,3, True, 3)

    name_room_type = request.args.get('type')
    capacity_in_room = request.args.get('capacity')
    room_types = dao.load_room_type()
    room = dao.get_room_by_namecapacity(capacity=capacity_in_room if capacity_in_room is not None else 1 ,name_room_type=name_room_type if name_room_type is not None else "Standard Room")
    rooms = dao.load_room_by_nameroomtype(name_room_type=name_room_type if name_room_type is not None else "Standard Room")
    room_type = dao.get_room_type_by_name(name=name_room_type)

    if current_user.is_authenticated:
        cart = dao.get_cart_by_userid(current_user.id)
        if not cart:
            dao.add_cart(current_user.id, 0)
    else:
        cart = {"id": None}

    return render_template("client/show.html", room_types=room_types, room=room, room_type=room_type, rooms=rooms, cart=cart)

@app.route('/login', methods=['get'])
def loginPage():
    return render_template("client/login.html")

@app.route('/login', methods=['post'])
def login_process():
    email = request.form.get('email')
    password = request.form.get('password')

    u = dao.auth_user(email=email, password=password)
    if u:
        login_user(u)
        return redirect('/')
    return  redirect('client/login.html')

@app.route('/register', methods=['get', 'post'])
def registerPage():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        passwordConfirm = request.form.get('passwordConfirm')

        if password.__eq__(passwordConfirm):
            data = request.form.copy()
            data['name'] = data['firstName'] + " " + data['lastName']
            del data['firstName']
            del data['lastName']
            del data['passwordConfirm']
            dao.add_user(**data)
            return redirect('/login')
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'
    return render_template("client/register.html",  err_msg=err_msg)

@app.route("/logout")
def logout_process():
    logout_user()
    return redirect('/login')

@app.route("/cart", methods=['get'])
def cart_page():
    if current_user.is_authenticated:
        cart = dao.get_cart_by_userid(current_user.id)
        cart_details = dao.load_cart_detail_by_cartid(cart.user_id)
        rooms = []
        room_types = []
        for cart_detail in cart_details:
            rooms.append(dao.get_room_by_id(cart_detail.room_id))
        for room in rooms:
            room_types.append(dao.get_room_type_by_id(room.room_type_id))
    else:
        return redirect("/")

    return render_template("client/cart.html", cart_details=cart_details, rooms=rooms, room_types=room_types)

@app.route("/cart", methods=['post'])
def cart_process():
    if current_user.is_authenticated:
        data = json.loads(request.form.get("post_cart_detail"))
        room_id = data.get("room_id")
        cart_id = data.get("cart_id")

        cart_detail = dao.get_cart_detail_by_roomid(room_id=room_id)
        if not cart_detail:
            dao.add_cart_detail(cart_id, room_id)
            quantity = dao.count_cart_detail_by_cartid(current_user.id)
            dao.update_quantity_cart_by_id(current_user.id, quantity)

    return redirect("/")

@app.route("/handle", methods=['post'])
def handle_del_cart_detail():
    data = json.loads(request.form.get("post_cart_detail"))
    cart_detail_id = data.get("cart_detail_id")
    cart_id = data.get("cart_id")
    dao.del_cart_detail_by_id(cart_detail_id)

    quantity = dao.count_cart_detail_by_cartid(current_user.id)
    dao.update_quantity_cart_by_id(cart_id, quantity)

    return redirect("/cart")

@app.route("/booking", methods=['post'])
def booking_process():
    if current_user.is_authenticated:
        data = json.loads(request.form.get("post_cart_detail"))
        room_id = data.get("room_id")
        cart_detail_id = data.get("cart_detail_id")

        room = dao.get_room_by_id(id=room_id)
        room_type = dao.get_room_type_by_id(id=room.room_type_id)
        return render_template("/client/booking.html", room=room, cart_detail_id=cart_detail_id, room_type=room_type)
    else:
        return redirect("/")

@app.route("/booking", methods=['get'])
def booking_page():
    if current_user.is_authenticated:
        room_id = request.args.get('room_id')
        room = dao.get_room_by_id(id=room_id)
        room_type = dao.get_room_type_by_id(id=room.room_type_id)

        return render_template("/client/booking.html", room=room, room_type=room_type)

@app.route("/completed-booking", methods=['post'])
def process_booking():
    data = request.form.copy()
    room_id = data['room_id']
    user_id = current_user.id

    dao.add_book(user_id=user_id, customer_phone=data['customer_phone'])
    book = dao.get_last_book()
    dao.add_book_detail(book_id=book.id, room_id=room_id, check_in_date=data['checkIn'], check_out_date=data['checkOut'], total_price=data['price_booking'], quantity=data['quantity_booking'], special_request=data['specialRequests'])

    room = dao.get_room_by_id(id=room_id)
    vacant_room = room.vacant_room - int(data['quantity_booking'])

    dao.update_vacant_room_by_id(room_id, vacant_room)

    return redirect("/completed-booking")

@app.route("/completed-booking", methods=['get'])
def completed_booking_page():
    return render_template("client/completed_booking.html")

#không được dùng tạo biến toàn cục cart ngay đây vì cần user_id -> khi người dùng log out sẽ lỗi
# @app.context_processor
# def common_context_params():
#     if current_user.is_authenticated:
#         if request.path.startswith('/admin'):
#             pass
#         else:
#             return {
#                 "cart": dao.get_cart_by_userid(current_user.id)
#             }

@login.user_loader
def get_user_by_id(user_id):
    return dao.get_user_by_id(user_id)

if __name__ == '__main__':
    app.run(debug=True)
