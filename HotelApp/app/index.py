import json
import threading
from datetime import datetime
from fpdf import FPDF
from flask import render_template, request, redirect, send_file
from HotelApp.app import app, login
import dao
from flask_login import login_user, logout_user, current_user
from HotelApp.app import admin

from HotelApp.app.dao import get_room_by_id
from HotelApp.app.models import UserRole


@app.route('/')
def homePage():

    thread = threading.Thread(target=update_vacant_room)
    thread.start()

    value_key_room = {
        "Single Room": {"1", "1 person", "1 bed", "one person", "one", "one bed", "Single Room"},
        "Double Room": {"2", "2 person", "2 bed", "two persons", "two", "two beds", "Double Room"},
        "Triple Room": {"3", "3 person", "3 bed", "three persons", "three", "three beds", "Triple Room"}
    }

    name_room_type = request.args.get('type')

    key_search = request.args.get('key_search')
    name_room = ""
    if key_search:
        for key, value in value_key_room.items():
            if key_search in value:
                name_room = key
                break

    capacity_in_room = request.args.get('capacity')

    room = dao.get_room_by_namecapacity(capacity=capacity_in_room if capacity_in_room is not None else 1 ,name_room_type=name_room_type if name_room_type is not None else "Standard Room")
    if key_search and name_room != "":
        room_type_id = dao.get_room_type_by_name(name_room_type).id
        room = dao.get_room_by_nameRoomTypeId(name_room, room_type_id)

    room_types = dao.load_room_type()
    rooms = dao.load_room_by_nameroomtype(name_room_type=name_room_type if name_room_type is not None else "Standard Room")
    room_type = dao.get_room_type_by_name(name=name_room_type)

    room_image = dao.load_room_image_by_roomid(room_id=room.id)
    room_images = []

    for room_ in rooms:
        room_images.append(dao.load_room_image_by_roomid(room_id=room_.id))

    cart = None
    if current_user.is_authenticated:
        cart = dao.get_cart_by_userid(current_user.id)

    return render_template("/client/show.html", room_types=room_types, room=room, room_type=room_type, rooms=rooms, cart=cart, room_image=room_image, room_images=room_images)

@app.route('/login', methods=['get'])
def loginPage():
    return render_template("/shared/login.html", check_account=True)

@app.route('/login', methods=['post'])
def login_process():
    email = request.form.get('email')
    password = request.form.get('password')

    u = dao.auth_user(email=email, password=password)
    if u:
        if u.status:
            login_user(u)
            if u.user_role == UserRole.STAFF:
                return redirect('/staff/customer')
            cart = dao.get_cart_by_userid(current_user.id)
            if not cart:
                dao.add_cart(current_user.id, 0)
            return redirect('/')
        else:
            return render_template("/shared/login.html", check_account=True, status_account=False)
    return render_template("/shared/login.html", check_account=False, status_account=True)

@app.route('/register', methods=['get', 'post'])
def registerPage():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        passwordConfirm = request.form.get('passwordConfirm')

        users = dao.load_user()
        data = request.form.copy()

        for user in users:
            if data['email'] == user.email:
                err_msg = "The email already exists!"
                return render_template("/shared/register.html", err_msg=err_msg)

        if password.__eq__(passwordConfirm):
            data['name'] = data['firstName'] + " " + data['lastName']
            del data['firstName']
            del data['lastName']
            del data['passwordConfirm']
            dao.add_user(**data)
            return redirect('/login')
        else:
            err_msg = 'The confirm password does not match!'
    return render_template("/shared/register.html",  err_msg=err_msg)

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
        room_images = []
        for cart_detail in cart_details:
            rooms.append(dao.get_room_by_id(cart_detail.room_id))
        for room in rooms:
            room_types.append(dao.get_room_type_by_id(room.room_type_id))
            room_images.append(dao.load_room_image_by_roomid(room.id))
    else:
        return redirect("/")

    return render_template("/client/cart.html", cart_details=cart_details, rooms=rooms, room_types=room_types, cart=cart, room_images=room_images)

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
        cart = dao.get_cart_by_userid(current_user.id)

        room = dao.get_room_by_id(id=room_id)
        room_type = dao.get_room_type_by_id(id=room.room_type_id)
        room_image = dao.load_room_image_by_roomid(room_id=room.id)
        config = dao.get_config_by_id(config_id=room_type.config_id)

        return render_template("/client/booking.html", room=room, cart_detail_id=cart_detail_id, room_type=room_type, cart=cart, room_image=room_image, config=config)
    else:
        return redirect("/")

@app.route("/booking", methods=['get'])
def booking_page():
    if current_user.is_authenticated:
        room_id = request.args.get('room_id')
        room = dao.get_room_by_id(id=room_id)
        room_type = dao.get_room_type_by_id(id=room.room_type_id)
        cart = dao.get_cart_by_userid(current_user.id)
        room_image = dao.load_room_image_by_roomid(room_id=room.id)
        config = dao.get_config_by_id(config_id=room_type.config_id)

        return render_template("/client/booking.html", room=room, room_type=room_type, cart=cart, room_image=room_image, config=config)

@app.route("/completed-booking", methods=['post'])
def process_booking():
    data = request.form.copy()
    room_id = data['room_id']
    user_id = current_user.id

    data['price_booking'] = float(data['price_booking'])

    dao.add_book(user_id=user_id, cccd=data['customer_cccd'], accurate_checkout_date=data['checkOut'])
    book = dao.get_last_book()
    dao.add_book_detail(book_id=book.id, room_id=room_id, check_in_date=data['checkIn'], check_out_date=data['checkOut'], total_price=data['price_booking'], quantity=data['quantity_booking'], number_of_foreigners=data['number_foreigners'], special_request=data['specialRequests'])

    room = dao.get_room_by_id(id=room_id)
    vacant_room = room.vacant_room - int(data['quantity_booking'])

    dao.update_vacant_room_by_id(room_id, vacant_room)

    return redirect("/completed-booking")

@app.route("/booked", methods=['get'])
def booked_page():
    books = dao.load_book_by_userid(current_user.id)
    book_details = []
    rooms = []
    room_types = []
    if books:
        for book in books:
            book_details.append(dao.get_book_details_by_bookid(book.id))
            rooms.append(dao.get_room_by_id(book_details[len(book_details) - 1].room_id))
            room_types.append(dao.get_room_type_by_id(rooms[len(rooms) - 1].room_type_id))

    cart = dao.get_cart_by_userid(current_user.id)
    return render_template("client/booked.html", cart=cart, books=books, book_details=book_details, rooms=rooms, room_types=room_types)

@app.route("/completed-booking", methods=['get'])
def completed_booking_page():
    cart = dao.get_cart_by_userid(current_user.id)
    return render_template("client/completed_booking.html", cart=cart)

#không được dùng tạo biến toàn cục cart ngay đây vì cần user_id -> khi người dùng log out sẽ lỗi
# @app.context_processor
# def common_context_params():
#     if current_user.is_authenticated:
#         if request.path.startswith('/staff'):
#             pass
#         else:
#             return {
#                 "cart": dao.get_cart_by_userid(current_user.id)
#             }

@login.user_loader
def get_user_by_id(user_id):
    return dao.get_user_by_id(user_id)

def update_vacant_room():
    while True:
        current_date = datetime.now()  # Lấy ngày hiện tại
        overdue_book_details = dao.load_book_detail_overdues(current_date)
        if overdue_book_details:
            for overdue_book_detail in overdue_book_details:
                dao.update_book_overdues(overdue_book_detail.book_id)
                room = get_room_by_id(overdue_book_detail.room_id)
                quantity = room.vacant_room + overdue_book_detail.quantity
                dao.update_vacant_room_by_id(room_id=room.id,quantity=quantity)
    time.sleep(86400)

@app.route('/checkout', methods=['post'])
def procees_check_out():
    data = json.loads(request.form.get("post_checkout"))
    room_id = data.get("room_id")
    book_id = data.get("book_id")
    book_detail_id = data.get("book_detail_id")
    dao.update_accurate_checkout_date(book_id=book_id, accurate_checkout_date=datetime.now().date() )
    book_detail = dao.get_book_details_by_bookid(book_id=book_detail_id)
    room = dao.get_room_by_id(id=room_id)

    quantity = int(book_detail.quantity) + int(room.vacant_room)

    dao.update_book_overdues(book_id)
    dao.update_vacant_room_by_id(room_id=room_id, vacant_room=quantity)

    return redirect("/checkout")

@app.route('/checkout', methods=['get'])
def checkout_page():
    cart = dao.get_cart_by_userid(current_user.id)
    return render_template("/client/completed_checkout.html", cart=cart)


# =================== STAFF =========================#
def authenticated_staff_account():
    if (current_user.is_authenticated and ((current_user.user_role == UserRole.STAFF) or (current_user.user_role == UserRole.ADMIN))):
        pass
    else:
        return redirect("/login")

@app.route('/staff/customer', methods=['get'])
def staff_customer_page():
    auth_result = authenticated_staff_account()
    if auth_result:
        return auth_result
    customers = dao.load_user_by_role(UserRole.USER)
    return render_template("/staff/show.html", customers=customers)

@app.route('/staff/customer/detail', methods=['get'])
def staff_detail_customer_page():
    auth_result = authenticated_staff_account()
    if auth_result:
        return auth_result
    customer_id = request.args.get('id')
    customer = dao.get_user_by_id(customer_id)
    return render_template("/staff/detail.html", customer=customer)

@app.route('/staff/customer/booked', methods=['get'])
def staff_booked_customer_page():
    auth_result = authenticated_staff_account()
    if auth_result:
        return auth_result
    customer_id = request.args.get('id')
    customer = dao.get_user_by_id(customer_id)
    books = dao.load_book_by_userid(customer_id)
    book_details = []
    rooms = []
    room_types = []
    configs = []
    for book in books:
        book_details.append(dao.get_book_details_by_bookid(book.id))
        rooms.append(dao.get_room_by_id(book_details[len(book_details) - 1].room_id))
        room_types.append(dao.get_room_type_by_id(rooms[len(rooms) - 1].room_type_id))

    return render_template("/staff/booked.html", customer=customer, books=books, book_details=book_details, rooms=rooms, room_types=room_types)

@app.route('/staff/customer/booked/export_book', methods=['post'])
def export_book_process():
    auth_result = authenticated_staff_account()
    if auth_result:
        return auth_result
    data = json.loads(request.form.get("post_export_book"))
    name = data.get('customer_name')
    email = data.get('customer_email')
    cccd = data.get('customer_cccd')
    room_name = data.get('room_name')
    numOfRooms = data.get('quantity_room')
    numOfCustomer = data.get('number_of_customer')
    name_room_type = data.get('room_name_type')
    total_price =  f"{float(data.get('price')):,.3f}"

    check_in_date = data.get('check_in_date').split(' ')[0]
    check_out_date = data.get('check_out_date').split(' ')[0]

    data_file = [
        name,
        email,
        cccd,
        room_name,
        numOfRooms,
        numOfCustomer,
        name_room_type,
        check_in_date,
        check_out_date,
        total_price
    ]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Tiêu đề
    pdf.cell(0, 10, "T-T-T Hotel Invoice", ln=True, align="C")
    pdf.cell(0, 10, "", ln=True, align="C")

    # Danh sách nhãn và giá trị
    labels = [
        "Full Name:",
        "Email:",
        "CCCD:",
        "Room Name:",
        "Number Of rooms:",
        "Number Of Customers:",
        "Name Of Room Type:",
        "Check In Date:",
        "Check Out Date:",
        "Total Price:"
    ]

    if(int(data.get('number_of_foreigners')) > 0):
        data_file.append(data.get('number_of_foreigners'))
        labels.append("Number Of Foreigners")

    # In từng hàng
    for i in range(len(labels)):
        pdf.cell(30, 10, labels[i], ln=False)  # Nhãn ở đầu dòng, cố định chiều rộng
        pdf.cell(0, 10, data_file[i], ln=True, align="C")  # Giá trị căn giữa

    # Lưu file
    pdf_file = f"invoice_{data.get('book_id')}_{''.join(data.get('customer_name').split(' '))}.pdf"
    pdf.output(pdf_file)

    return send_file(pdf_file, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/staff/block-customer-account', methods=['post'])
def block_cust_account_process():
    auth_result = authenticated_staff_account()
    if auth_result:
        return auth_result
    data = json.loads(request.form.get("post_block_customer_account"))
    user_id = data.get('customer_id')

    user = dao.get_user_by_id(user_id)
    if user.status == True:
        dao.update_status_user_by_id(user_id=user_id, status=False)
    else:
        dao.update_status_user_by_id(user_id=user_id, status=True)
    return redirect("/staff/customer")

@app.route("/staff/customer/search", methods=['post'])
def search_customer_process():
    auth_result = authenticated_staff_account()
    if auth_result:
        return auth_result
    data = request.form.get("searchFor")
    customers = dao.load_user_by_name(name=data)
    if not customers:
        customers = dao.load_user_by_email(email=data)
    return render_template("/staff/show.html", customers=customers)

@app.route('/staff/book', methods=['get'])
def book_page():
    auth_result = authenticated_staff_account()
    if auth_result:
        return auth_result
    books = dao.load_all_book()
    book_details = []
    rooms = []
    room_types = []
    customers = []
    for book in books:
        customers.append(dao.get_user_by_id(book.user_id))
        book_details.append(dao.get_book_details_by_bookid(book.id))
        rooms.append(dao.get_room_by_id(book_details[len(book_details) - 1].room_id))
        room_types.append(dao.get_room_type_by_id(rooms[len(rooms) - 1].room_type_id))
    return render_template('/staff/book.html', customers=customers, book_details=book_details, rooms=rooms, room_types=room_types, books=books)

@app.route("/staff/room", methods=['get'])
def room_page():
    auth_result = authenticated_staff_account()
    if auth_result:
        return auth_result
    rooms = dao.load_all_room()
    room_types = []
    for room in rooms:
        room_types.append(dao.get_room_type_by_id(room.room_type_id))
    return render_template("/staff/room.html", rooms=rooms, room_types=room_types)

@app.route("/staff/room_type")
def room_type_page():
    auth_result = authenticated_staff_account()
    if auth_result:
        return auth_result
    room_types = dao.load_room_type()
    return render_template("/staff/room_type.html", room_types=room_types)

@app.route("/staff/config")
def config_page():
    auth_result = authenticated_staff_account()
    if auth_result:
        return auth_result
    configs = dao.load_config()
    return render_template("/staff/config.html", configs=configs)


#Admin
@app.route("/login-admin", methods=['post'])
def login_admin_process():
    email = request.form.get('email')
    password = request.form.get('password')
    u = dao.auth_user(email=email, password=password, role=UserRole.ADMIN)
    if u:
        login_user(u)
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
