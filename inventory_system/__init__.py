import os
import urllib.request
from werkzeug.utils import secure_filename
from flask import Flask, url_for
# from inventory_system.database import get_data,insert_products,insert_sales,display_sales,display_profit,day_sales,pro_per_day\
#     ,Total_profit,pro_for_today,display_sum_sales,display_sum_sales_today,get_remaining_stock_per_product,delete_record,\
#         products_name
from flask_sqlalchemy import SQLAlchemy # pip install flask-sqlalchemy
from sqlalchemy import create_engine, MetaData,func, Table, Column, Integer, String, select, insert, update, delete,desc
from flask_bcrypt import Bcrypt # pip install flask-bcrypt
from flask_migrate import Migrate #( pip install Flask-Migrate ) we use this function to be able to modify or delete any column from the database 
from flask_login import  LoginManager,UserMixin,login_user,current_user,logout_user,login_required #pip install flask-login
from flask_mail import Mail,Message # pip install flask-mail

# from .models import db


app = Flask(__name__)


app.config['SECRET_KEY'] =\
    '580c83d8b1bd97f330436702260c70204cb44f7281c391b147eac2373b45ee27' 
# user:password@localhost:5432/postgres
# myduka_system.db
connection_string = app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:0777@localhost/inventory_system"
db=SQLAlchemy(app)
migrate = Migrate(app, db)  # To use the migrate open terminal and write (flask db init)after that write (flask db migrate -m "any comment like: Initial migration") last thing write (flask db upgrade)

# Create the engine
engine = create_engine(connection_string)

# try:
#     with engine.connect() as conn:
#         print("Connection successful!")
# except Exception as e:
#     print("Connection failed:", e) 

# app.config["SQLALCHEMY_TARCK_MODFICATIONS"] = True


# Define metadata
metadata = MetaData()

app.app_context().push()
bcrypt= Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # if the user is not logged in and try to access the page that requires login then it will redirect to the login page
login_manager.login_message_category = 'info' # to change the message category

# we used system environment: so that anyone who saw my code could not know what the password was for my account
app.config["MAIL_SERVER"] = "smtp.googlemail.com" # if you are sending from gmail there is a steps to follow : 1- go to your gmail account 2- go to security 3- then go to the less secure app access 4- turn it on and search about (App password) copy the password and then go to pc search about (environment variables) and then go to system variables and then click new and then write (EMAIL_USER and your email) and then write again (EMAIL_PASS and paste that password that u copy it from google) 
app.config["MAIL_PORT"] = 587 # 587 is the port number
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_USER") # os.environ.get("EMAIL_USER") is to get the email from the environment variables
app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PASS") # os.environ.get("EMAIL_PASS") is to get the password from the environment variables

UPLOAD_FOLDDER = 'static/user_pics'
app.config['UPLOAD_FOLDDER'] = UPLOAD_FOLDDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWD_EXTENSIONS = set(["jpeg", "png", "jpg", "gif"])
mail = Mail(app) # to send the email


