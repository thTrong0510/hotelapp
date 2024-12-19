from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = 'HJGFGHF^&%^&&*^&*YUGHJGHJF^%&YYHBhjh'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/hoteldb?charset=utf8mb4" % quote('Thanhtrong@0510')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 6

db = SQLAlchemy(app)
login = LoginManager(app)

cloudinary.config(
    cloud_name="dxxwcby8l",
    api_key="448651448423589",
    api_secret="ftGud0r1TTqp0CGp5tjwNmkAm-A",  # Click 'View API Keys' above to copy your API secret
    secure=True
)