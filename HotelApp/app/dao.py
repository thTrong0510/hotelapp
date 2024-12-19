from HotelApp.app.models import User, RoomType, Cart, CartDetail, ConfigParameters, Room, RoomImage, BookDetail, Book
from HotelApp.app import app, db
import hashlib
import cloudinary.uploader

def get_user_by_id(user_id):
    return User.query.get(user_id)

def add_user(name, password, email, avatar=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User(name=name, password=password, email=email)
    if avatar:
        res = cloudinary.uploader.upload(avatar)
        u.avatar = res.get('secure_url')
    db.session.add(u)
    db.session.commit()

def add_config_parameters(rev_period_checkin, surcharge):
    config = ConfigParameters(rev_period_checkin=rev_period_checkin, surcharge=surcharge)
    db.session.add(config)
    db.session.commit()

def add_room_type(name, price, quantity, config_id):
    room_type = RoomType(name=name, price=price, quantity=quantity, config_id=config_id)
    db.session.add(room_type)
    db.session.commit()

def load_room_type():
    return RoomType.query.order_by('id').all()

def get_room_type_by_id(id):
    room_type = RoomType.query
    if id:
        room_type = room_type.filter_by(id=id)
    return room_type.first()

def get_room_type_by_name(name="Standard Room"):
    room_type = RoomType.query
    if name:
        room_type = RoomType.query.filter_by(name=name)
    return room_type.first()

def add_room(name, description, short_desc, price, capacity, quantity, vacant_room, active, room_type_id):
    room = Room(name=name, description=description, short_desc=short_desc, price=price, capacity=capacity, quantity=quantity, vacant_room=vacant_room, active=active, room_type_id=room_type_id)
    db.session.add(room)
    db.session.commit()

def load_room_by_nameroomtype(name_room_type=None):
    rooms = Room.query
    if name_room_type:
        room_type = get_room_type_by_name(name_room_type)
        room_type_id = room_type.id
        rooms = rooms.filter_by(room_type_id=room_type_id)
    return rooms.all()

def load_room_by_capacity(capacity=1):
    return Room.query.filter_by(capacity=capacity).all()

def get_room_by_namecapacity(capacity=1, name_room_type="Standard Room"):
    room_type = get_room_type_by_name(name_room_type)
    room_type_id = room_type.id
    rooms = Room.query.filter_by(room_type_id=room_type_id)
    room = rooms.filter_by(capacity=capacity)
    return room.first()

def get_room_by_id(id):
    return Room.query.filter_by(id=id).first()

def add_cart(user_id, total_quantity=0, total_price=0):
    cart = Cart(user_id=user_id, total_quantity=total_quantity, total_price=total_price)
    db.session.add(cart)
    db.session.commit()

def get_cart_by_userid(user_id):
    return Cart.query.filter_by(user_id=user_id).first()

def get_cart_detail_by_roomid(room_id):
    return CartDetail.query.filter_by(room_id=room_id).first()

def load_cart_detail_by_cartid(cart_id):
    return CartDetail.query.filter_by(cart_id=cart_id).all()

def update_quantity_room_cart_detail(cart_detail, quantity):
    cart_detail.quantity += quantity
    db.session.commit()

def add_cart_detail(cart_id, room_id, quantity, price):
    cart_detail = CartDetail(cart_id=cart_id, room_id=room_id, quantity=quantity, price=price)
    db.session.add(cart_detail)
    db.session.commit()

def del_cart_detail_by_id(cart_detail_id):
    cart_detail = CartDetail.query.get(cart_detail_id)
    db.session.delete(cart_detail)
    db.session.commit()
    #update cart

def auth_user(email, password, role=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User.query.filter(User.email.__eq__(email),User.password.__eq__(password))
    if role:
        u = u.filter(User.user_role.__eq__(role))

    return u.first()

