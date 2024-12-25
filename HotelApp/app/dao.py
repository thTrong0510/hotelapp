from HotelApp.app.models import User, RoomType, Cart, CartDetail, ConfigParameters, Room, RoomImage, BookDetail, Book, \
    UserRole
from HotelApp.app import app, db
import hashlib
import cloudinary.uploader

def get_user_by_id(user_id):
    return User.query.get(user_id)

def add_user(name, password, email):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, password=password, email=email)
    db.session.add(u)
    db.session.commit()

def add_staff(name, password, email, user_role=UserRole.STAFF):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, password=password, email=email, user_role=user_role)
    db.session.add(u)
    db.session.commit()

def load_user():
    return User.query.all()

def load_user_by_role(userRole):
    return User.query.filter_by(user_role=userRole).all()

def load_user_by_email(email):
    return User.query.filter_by(email=email).all()

def load_user_by_name(name):
    return User.query.filter_by(name=name).all()

def update_status_user_by_id(user_id, status):
    user = User.query.filter_by(id=user_id).first()
    user.status = status
    db.session.commit()

def add_config_parameters(rev_period_checkin, surcharge):
    config = ConfigParameters(rev_period_checkin=rev_period_checkin, surcharge=surcharge)
    db.session.add(config)
    db.session.commit()

def load_config():
    return ConfigParameters.query.all()

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

def add_room(name, description, short_desc, price, capacity, quantity, vacant_room, room_type_id):
    room = Room(name=name, description=description, short_desc=short_desc, price=price, capacity=capacity, quantity=quantity, vacant_room=vacant_room, room_type_id=room_type_id)
    db.session.add(room)
    db.session.commit()

def load_all_room():
    return Room.query.all()

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

def get_room_by_nameRoomTypeId(name, room_type_id):
    return Room.query.filter_by(name=name, room_type_id=room_type_id).first()

def get_room_by_id(id):
    return Room.query.filter_by(id=id).first()

def update_vacant_room_by_id(room_id, vacant_room):
    room = Room.query.filter_by(id=room_id).first()
    room.vacant_room = vacant_room
    db.session.commit()

def add_room_image_by_roomid(room_id, image):
    room_image = RoomImage(room_id=room_id, image=image)
    db.session.add(room_image)
    db.session.commit()

def load_room_image_by_roomid(room_id):
    return RoomImage.query.filter_by(room_id=room_id).all()

def add_cart(user_id, total_quantity=0):
    cart = Cart(user_id=user_id, total_quantity=total_quantity)
    db.session.add(cart)
    db.session.commit()

def update_quantity_cart_by_id(id, quantity):
    cart = Cart.query.filter_by(user_id=id).first()
    cart.total_quantity = quantity
    db.session.commit()

def get_cart_by_userid(user_id):
    return Cart.query.filter_by(user_id=user_id).first()

def get_cart_detail_by_roomid(room_id):
    return CartDetail.query.filter_by(room_id=room_id).first()

def load_cart_detail_by_cartid(cart_id):
    return CartDetail.query.filter_by(cart_id=cart_id).all()

def add_cart_detail(cart_id, room_id):
    cart_detail = CartDetail(cart_id=cart_id, room_id=room_id)
    db.session.add(cart_detail)
    db.session.commit()

def del_cart_detail_by_id(cart_detail_id):
    cart_detail = CartDetail.query.get(cart_detail_id)
    db.session.delete(cart_detail)
    db.session.commit()
    #update cart

def count_cart_detail_by_cartid(cart_id):
    return CartDetail.query.filter_by(cart_id=cart_id).count()

def load_book_by_userid(user_id):
    return Book.query.filter_by(user_id=user_id).all()

def load_all_book():
    return Book.query.all()

def add_book(user_id, customer_phone, accurate_checkout_date):
    book = Book(user_id=user_id, customer_phone=customer_phone, accurate_checkout_date=accurate_checkout_date)
    db.session.add(book)
    db.session.commit()

def get_last_book():
    return Book.query.order_by(Book.id.desc()).first()

def update_accurate_checkout_date(book_id, accurate_checkout_date):
    book = Book.query.filter_by(id=book_id).first()
    book.accurate_checkout_date = accurate_checkout_date
    db.session.commit()

def update_book_overdues(book_id):
    book = Book.query.filter_by(id=book_id).first()
    book.status = False
    db.session.commit()

def get_book_details_by_bookid(book_id):
    return BookDetail.query.filter_by(book_id=book_id).first()

def add_book_detail(book_id, room_id, check_in_date, check_out_date, total_price, quantity, number_of_foreigners, special_request):
    book_detail = BookDetail(book_id=book_id, room_id=room_id, check_in_date=check_in_date, check_out_date=check_out_date, total_price=total_price, quantity=quantity, number_of_foreigners=number_of_foreigners, special_request=special_request)
    db.session.add(book_detail)
    db.session.commit()
    return book_detail

def load_book_detail_overdues(current_date):
    return db.session.query(BookDetail).filter(BookDetail.checkOutDate < current_date).all()

def auth_user(email, password, role=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User.query.filter(User.email.__eq__(email),User.password.__eq__(password))
    if role:
        u = u.filter(User.user_role.__eq__(role))

    return u.first()

