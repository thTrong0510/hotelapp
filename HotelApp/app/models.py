from email.policy import default

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from HotelApp.app import db, app
from enum import Enum as RoleEnum
from flask_login import UserMixin

class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2

class UserType(RoleEnum):
    Domestic = 1
    Foreign = 2

class ConfigParameters(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rev_period_checkin = db.Column(db.Integer, default=28)
    surcharge = Column(Float, default=1)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    user_type = Column(Enum(UserType), default=UserType.Domestic)
    room_type = relationship('RoomType', backref='ConfigParameters', lazy=True)


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    password = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1679134375/ckvdo90ltnfns77zf1xb.jpg')
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    user_type = Column(Enum(UserType), default=UserType.Domestic)
    cart = db.relationship('Cart', uselist=False, backref='user', cascade='all, delete-orphan')
    book_details = relationship('Book', backref='user', lazy=True)

# Model Cart (quan hệ một-nhiều với User, chỉ để hiển thị ra giao diện số lượng phòng)
class Cart(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True ,nullable=False)  # Khóa ngoại liên kết đến User
    total_quantity = db.Column(db.Integer, default=0)
    cart_details = db.relationship('CartDetail', backref='cart', lazy=True)

# Model CartDetail (quan hệ một-nhiều với Cart và nhiều-đến-1 với Room)
class CartDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.user_id'), nullable=False)  # Khóa ngoại liên kết đến Cart
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)  # Khóa ngoại liên kết đến Room

class RoomType(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    price = db.Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    daily_multiplier = Column(Float, nullable=False, default=1)
    session_multiplier = Column(Float, nullable=False, default=0.5)
    room_count_multiplier = Column(Float, nullable=False, default=0.7)
    foreign_guest_multiplier = Column(Float, nullable=False, default=0.2)
    config_id = db.Column(db.Integer, ForeignKey('config_parameters.id'), nullable=False)
    room = db.relationship('Room', backref='RoomType', lazy=True)

class Room(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(db.Text, nullable=True)
    short_desc = Column(db.Text, nullable=False)
    price = Column(Float, nullable=False)
    capacity = Column(db.Integer, default=1)
    quantity = Column(Integer, default=1)
    vacant_room  = Column(Integer, default=1)
    active = Column(Boolean, default=True)
    room_type_id = Column(Integer, ForeignKey(RoomType.id), nullable=False)
    book_details = relationship('BookDetail', backref='room', lazy=True)
    cart_details = db.relationship('CartDetail', backref='room', lazy=True)

class RoomImage(db.Model):
    id = Column(db.Integer, primary_key=True, autoincrement=True)
    image_url = Column(db.String(255), nullable=False)  # đường dẫn ảnh
    created_at = Column(db.DateTime, default=db.func.current_timestamp())
    room_id = Column(db.Integer, db.ForeignKey(Room.id), nullable=False)  # khóa ngoại

class Book(db.Model):
    id = Column(db.Integer, primary_key=True, autoincrement=True)
    customer_phone = Column(db.String(100), nullable=False)
    booking_date = Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    book_detail = db.relationship('BookDetail', uselist=False, backref='book', cascade='all, delete-orphan')

class BookDetail(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True, nullable=False)  # khóa ngoại liên kết đến Book
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'),nullable=False)  # ID của phòng
    check_in_date = db.Column(db.DateTime, nullable=False)
    check_out_date = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    special_request = db.Column(db.Text, default="null")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.commit()
