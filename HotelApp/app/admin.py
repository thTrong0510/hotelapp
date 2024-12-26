import hashlib

from sqlalchemy.orm import configure_mappers
from flask import request
from HotelApp.app import  db, app
from HotelApp.app.models  import User, Room  ,ConfigParameters,RoomType,RoomImage
from flask_admin import Admin, BaseView , expose, AdminIndexView
from flask_login import current_user, logout_user
from flask import redirect
from HotelApp.app.models import UserRole
from HotelApp.app import dao
from flask_admin.contrib.sqla import ModelView
from datetime import datetime

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html',
                           stats=dao.count_Rom_by_Romtype())
admin = Admin (app=app, name='Admin', template_mode='bootstrap4',index_view=MyAdminIndexView())

class AdminView(ModelView):
    can_export = True
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)
class AuthenticatedView(BaseView):

    def is_accessible(self):
        return current_user.is_authenticated
class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        year=request.args.get('year',datetime.now().year)
        return self.render('admin/stats.html',
                           stats=dao.stats_room_type(),stats2=dao.revenue_time(year))

class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

class RoomTypeView(AdminView):
    column_list = ['name',]
    form_excluded_columns = ['room']
class ConfigView(AdminView):
    can_export = True

class RoomView(AdminView):
    column_list = ['id', 'name', 'price', 'RoomType']
    can_export = True
    column_searchable_list = ['name']
    column_filters = ['id', 'name', 'price']
    page_size = 10
    column_editable_list = ['name']
    column_display_all_relations = True
    can_view_details = True
    form_excluded_columns = ['cart_details', 'book_details']
class UersView(AdminView):
    form_excluded_columns = ['cart','book_details']

    def on_model_change(self, form, model, is_created):
        if form.password.data:  # Kiểm tra nếu có mật khẩu được nhập
            password = form.password.data.strip()  # Loại bỏ khoảng trắng thừa
            # Băm mật khẩu bằng MD5
            model.password = hashlib.md5(password.encode('utf-8')).hexdigest()
        super(UersView, self).on_model_change(form, model, is_created)
class RoomImgView(AdminView):
    can_export = True
 #fix anf  colum ko can  thiet o muc create
configure_mappers()
admin.add_view(UersView(User ,db.session))
admin.add_view(RoomView(Room, db.session))
admin.add_view(RoomTypeView(RoomType, db.session))
admin.add_view(ConfigView(ConfigParameters, db.session))
# admin.add_view(RoomImgView(RoomImage, db.session))
admin.add_view(StatsView(name='Thống Kê'))
admin.add_view(LogoutView(name='Đăng xuất'))