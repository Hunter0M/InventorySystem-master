from datetime import datetime
from inventory_system import app
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView 
from flask_login import  LoginManager,UserMixin,login_user,current_user,logout_user,login_required #pip install flask-login
from itsdangerous import URLSafeTimedSerializer as Serializer # This is used to reset the password after this go to th User model 
from flask_admin import Admin # pip install flask-admin
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView


from inventory_system import db, login_manager, bcrypt, Message, mail, url_for



# it updates the user using the user ID that stored in session
@login_manager.user_loader 
def load_user(user_id): # this function is used to load the user from the database
    return User.query.get(int(user_id))


# Model for User
class User(db.Model, UserMixin):
    __tablename__="users"
    id = db.Column(db.Integer,primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    # lname = db.Column(db.String(50), nullable=False)
    # username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    image_file = db.Column(db.String(1000), nullable=False, default = 'default.png')
    bio = db.Column(db.Text, nullable=True)
    # func=> it's bring the current time
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    # sales = db.relationship('Sale', backref='User')


    def get_reset_token(self): # this function is used to generate the token
        s = Serializer(app.config['SECRET_KEY'], salt='pw-reset')
        return s.dumps({'user_id': self.id})

    @staticmethod # We used this to know that we are using it as a static method
    def verify_reset_token(token, age=1800):
        s = Serializer(app.config['SECRET_KEY'], salt='pw-reset')
        try: # use this if the token is valid
            user_id = s.loads(token, max_age=age)['user_id']
        except: # use this if the token is not valid
            return None
        return User.query.get(user_id) # return the user if it's valid
    
    def __repr__(self):
        # f"Users('{self.fname}', '{self.lname}', '{self.username}', '{self.email}', '{self.image_file}')"
        return f'User  {self.id} {self.fname}  {self.email}'
# admin.add_view(ModelView(User,db.session)) # add the model to the admin

# Model for Product    
class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer,primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    buying_price = db.Column(db.Numeric(10,2), nullable=False)
    selling_price = db.Column(db.Numeric(10,2), nullable=False)
    stock_quantity = db.Column(db.Integer , nullable=False)
    sales = db.relationship('Sale',backref="Product")


    def __init__(self, product_name, buying_price, selling_price, stock_quantity):
        self.product_name = product_name
        self.buying_price = buying_price
        self.selling_price = selling_price
        self.stock_quantity = stock_quantity


# Model for Sale
class Sale(db.Model):
    __tablename__ = "sales" 
    id = db.Column(db.Integer,primary_key=True) 
    pid = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Numeric(10,2) ,nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


   
    def __repr__(self):
        return f'Sales {self.pid} {self.created_at}'
    

class UserModelView(ModelView): # This is the admin model view
    def on_model_change(self, form, model, is_created): # This function is used to hash the password before saving it to the database
        model.password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8)"
        )

# This function is used to check if the user is authenticated and if the user is the admin
    def is_accessible(self): 
        return current_user.is_authenticated and current_user.id == 2

 # This is the admin model view
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 2


class MyAdminIndexView(AdminIndexView): 
    def is_accessible(self): # This function is used to check if the user is authenticated and if the user is the admin
        return current_user.is_authenticated and current_user.id == 2

# to use the admin panel
admin = Admin(app, index_view=MyAdminIndexView()) 

# This is the admin view
admin.add_view(UserModelView(User, db.session)) 
admin.add_view(MyModelView(Product, db.session)) 
admin.add_view(MyModelView(Sale, db.session))



# Reset Password      
# we use this function to send a mail to the user
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Myduka System App Password Reset Request",
        sender="735mo735@gmail.com",
        recipients=[user.email],
        body=f"""To reset your password, visit the following link:
        {url_for('reset_password', token=token, _external=True)} 
        
        if you did not make this request, please ignore this email.""", # this is the link that will be sent to the user to reset the password and the _external(we use this for the absolute URL)
    )
    mail.send(msg) 