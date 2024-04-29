import secrets


from flask import render_template,request,redirect,flash,abort
from PIL import Image  # pip install pillow
from werkzeug.utils import secure_filename # this will secure the filename and it will be used in the save_picture function   
from flask_login import  LoginManager,UserMixin,login_user,current_user,logout_user,login_required #pip install flask-login


from inventory_system.models import User,Product,Sale,UserModelView,MyModelView, send_reset_email
from inventory_system.forms import UpdateProfileForm, LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm
from inventory_system import app, db, bcrypt, desc, func, os,url_for
from inventory_system.database import display_profit, Total_profit, pro_for_today, display_sum_sales, display_sum_sales_today, display_sales, day_sales, pro_per_day, get_remaining_stock_per_product, insert_sales


@app.route("/")
def home():
    return render_template('home.html')


def save_picture(form_picture): # this function is used to save the picture in the static folder
    random_hex = secrets.token_hex(8) # this will generate a random hex code
    # _, f_ext => when we use ( _, ) in python it means that we don't need the first variable or ignore this variable
    _, f_ext = os.path.splitext(form_picture.filename) # this will split the filename and the extension
    picture_name = random_hex + f_ext # this will generate a random hex code and the extension of the file
    picture_path = os.path.join(app.root_path, "static/user_pics", picture_name) # this will generate the path of the picture
    # app.root_path => it represents our root address
    
    output_size = (150, 150) # this will resize the picture
    i = Image.open(form_picture) # this will open the picture and to use Image we have to import it using this command ( from PIL import Image ) and we have to install pillow using this command ( pip install pillow )
    i.thumbnail(output_size) # this will resize the picture
    i.save(picture_path) # this will save the picture in the static folder
    return picture_name 


# @app.route('/upload', methods=['POST']) 
# @login_required
# def upload():
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     file = request.files['file']
#     if file.filename == '':
#         flash('No selected file')
#         return redirect(request.url)
#     if file:
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         current_user.image_file = filename
#         db.session.commit()
#         flash('Profile picture updated')
#         return redirect(url_for('home'))



@app.route("/updateprofile", methods=['GET', 'POST']) 
@login_required
def updateprofile():
    profile_form = UpdateProfileForm()
    if profile_form.validate_on_submit(): # this will check if the form is valid
        if profile_form.picture.data: # this will check if the picture is not empty
            picture_file = save_picture(profile_form.picture.data) # this will save the picture in the static folder
            current_user.image_file = picture_file # this will save the picture in the database
        current_user.fname =profile_form.fname.data 
        current_user.email =profile_form.email.data
        current_user.bio =profile_form.bio.data
        db.session.commit()
        flash("Your profile has been updated!", "success")
        return redirect(url_for("updateprofile"))
    elif request.method == "GET": # this will check if the request is a get request
        profile_form.fname.data = current_user.fname 
        profile_form.email.data = current_user.email 
        profile_form.bio.data = current_user.bio
    image_file = url_for('static', filename=f'user_pics/{current_user.image_file}') # this will get the image file from the static folder
    return render_template("profile.html",profile_form = profile_form, image_file=image_file) # this will render the profile.html template

# profile = Profile.query.get(current_user.id)
# profile.image_file = 'filename.jpg'
# db.session.commit()

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # here we check if the email is in the database
        if user and bcrypt.check_password_hash(user.password, form.password.data): # here we check if the password is correct
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') #first you write code like how its written in line 32# used the next_page for(the time you logged out and you traid to accses to another page
            # by entering url you cant accses until you login and it take you to the page that you tried to accses)
            flash("You have been logged in!", "success")
            return redirect(next_page) if next_page else redirect( url_for("home"))
        else:
            flash("Login Unsuccessful. Please check credentials", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route('/register', methods=['GET' , 'POST']) # here we use the method post because we want to send data to the server
def register(): # here we create a function to register the user
    if current_user.is_authenticated: # is_authenticated is a property of the User class in Flask-Login that returns True if the user is currently authenticated, and False otherwise. It is used to check if a user is logged in or not.
        return redirect(url_for("home"))
    form=RegistrationForm()
    if form.validate_on_submit(): # here check if everything about the form it will print this massages
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # here we hash the password
        user=User(fname=form.fname.data,  email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created successfully for {form.fname.data}",'success')
        return redirect(url_for('login'))
    return render_template("register.html",form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been successfully logged out ",'success')
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():
    # route to display profit
    dash_profit=display_profit()
    names_profit=[]
    value_profit=[]
    for i in dash_profit:
        names_profit.append(str(i[0]))
        value_profit.append(float(i[1]))

    # route to display total profits
    profit_per_day=Total_profit()

    # route to display profit for today
    profit_today=pro_for_today()

    # calculating total sales to display as one
    total_sales=display_sum_sales()

    today_sales=display_sum_sales_today()

    

   # route to display sales  
    dash_sales=display_sales()  
    names=[]
    value=[]
    for i in dash_sales:
        names.append(str(i[0]))
        value.append(float (i[1]))

    # route to display sales per a day 
    sales_day=day_sales()
    s_name=[]
    v_value=[]
    for i in sales_day:
        s_name.append(str(i[0]))
        v_value.append(float (i[1]))

    # route to display profit per day
        profit_day=pro_per_day()
        pro_name=[]
        pro_value=[]
        for i in profit_day:
            pro_name.append(str(i[0]))
            pro_value.append(float (i[1]))


    # This query calculates the remaining stock for
    #  each product by subtracting the total quantity sold
    #  from the total quantity available.
    remaining_stock = get_remaining_stock_per_product()
    remaining_stock_labels=[]
    remaining_stock_data=[]
    for i in remaining_stock:
        remaining_stock_labels.append(str(i[0]))
        remaining_stock_data.append(float (i[1]))


    


    # This query returns the total number of sales
    # recent_sales = Sale.query.all()
    # print(recent_sales) 
    # recent_sales = db.session.query(Sale, User.fname, Product.product_name, \
    #             Sale.quantity, Sale.created_at).join(User, Sale.pid == User.id)\
    #                 .join(Product, Sale.pid == Product.id).order_by\
    #                     (Sale.created_at.desc()).limit(10).all() 
    # recent_sales = db.session.query(Sale, User.fname, Product.product_name, \
    #             Sale.quantity, Sale.created_at).join(User, Sale.pid == User.id).join(Product, Sale.pid == Product.id).order_by\
    #                     (Sale.created_at.desc()).limit(10).all()

    recent_sales = db.session.query(Sale, User.fname, Product.product_name, \
    Sale.quantity, Sale.created_at) \
    .join(Product, Sale.pid== Product.id) .order_by(desc(Sale.created_at)).limit(10) \
    .all()
    # print(recent_sales)
    # This query calculates the total amount of sales
    #  and the average amount of sales per day.
    total_amount = db.session.query(func.sum(Sale.quantity * Product.selling_price)).scalar()
    # average_amount = total_amount / db.session.query(Sale).count()
    total_amount = db.session.query(func.sum(Sale.quantity * Product.selling_price)) \
    .join(Product) \
    .scalar()
    # Calculate total sales count
    total_sales_count = db.session.query(func.count(Sale.id)).scalar()

    # Calculate average amount
    average_amount = total_amount / total_sales_count if total_sales_count else 0

    # print("Total Amount:", total_amount)
    # print("Total Sales Count:", total_sales_count)
    # print("Average Amount per Sale:", average_amount)

    return render_template('dashboard.html',dash_sales=dash_sales,names=names,value=value,
                           names_profit=names_profit,value_profit=value_profit,s_name=s_name,
                           v_value=v_value,pro_name=pro_name,pro_value=pro_value,profit_per_day=profit_per_day,
                           profit_today=profit_today,total_sales=total_sales,today_sales=today_sales,
                           remaining_stock_labels=remaining_stock_labels, remaining_stock_data=remaining_stock_data,
                            products=Product,sal=Sale,recent_sales=recent_sales,average_amount=average_amount, title='Dashboard')

# 
@app.route("/profile") 
@login_required
def profile():
    return render_template('profile.html', title='Profile')


# 


@app.route('/products')
@login_required
def product():
    all_data = Product.query.all()
    return render_template("products.html", prods = all_data)

@app.route('/insert', methods=['POST'])
@login_required
def insert():
    if request.method == 'POST':
        pname = request.form['product_name']
        b_price = request.form['buying_price']
        s_price = request.form['selling_price']
        s_quantity = request.form['stock_quantity']
        my_data = Product(pname, b_price, s_price, s_quantity)
        db.session.add(my_data)
        db.session.commit()
        flash(f'Product Inserted Successfuly for:{pname}','success')
        return redirect(url_for('product'))
    
@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():

    if request.method == 'POST':
        my_data = Product.query.get(request.form.get('id'))

        my_data.product_name = request.form['product_name']
        my_data.buying_price = request.form['buying_price']
        my_data.selling_price = request.form['selling_price']
        my_data.stock_quantity = request.form['stock_quantity']

        db.session.commit()
        flash(f'Product Inserted Successfuly for:{my_data.product_name}','success')

        return redirect(url_for('product'))

@app.route('/delete/<id>/', methods = ['GET', 'POST'])
@login_required
def delete(id):
    my_data = Product.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash(f'Product Deleted Successfully For: {my_data.product_name}','success')

    return redirect(url_for('product'))



# creating a route for sales
@app.route("/sales")
@login_required
def sales():
    sales=Sale.query.all()
    print(sales)
    products=Product.query.all()
    print(products)
    return render_template('sales.html',sales=sales,products=products,title="Sales")

# a route for adding sales
@app.route("/make_sale", methods=['POST'])
@login_required
def make_sale(): 
    try:     
        # Fetch form data
        pid = int(request.form['pid'])
        quantity = int(request.form['quantity'])

        # Fetch products and validate quantity
        product = Product.query.get(pid)
        if not product:
            flash("Invalid product ID", 'error')
            return redirect(url_for("sales"))

        stock = product.stock_quantity
        if quantity <= 0 or quantity > stock:
            flash("Invalid quantity", 'error')
            return redirect(url_for("sales"))

        # Proceed with the sale
        values = (pid, quantity)
        print("values",values)
        insert_sales(values)
        flash(f'Sales made successfully for {quantity} {product.product_name}', 'success')

    except ValueError: 
        flash("Invalid quantity", 'error')
    except Exception as e: 
        flash(f'Failed to make sale: {str(e)}', 'error')

    return redirect(url_for("sales"))


@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated: # this used to check if the user is logged in or not
        return redirect(url_for("home"))
    form = RequestResetForm() 
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user) # this function used to send the email to the user and to use this we have to install flask-mail using this command ( pip install flask-mail )
        flash(
            "If this account exists, you will receive an email with instructions",
            "info",
        )
        return redirect(url_for("login"))
    return render_template("reset_request.html", title="Reset Password", form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated: # this used to check if the user is logged in or not  
        return redirect(url_for("home"))
    user = User.verify_reset_token(token) # this used to check if the user is not logged in 
    if not user:
        flash("The token is invalid or expired", "warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash(f"Your password has been updated. You can now log in", "success")
        return redirect(url_for("login"))
    return render_template("reset_password.html", title="Reset Password", form=form)


# This is used to show the error page when the user enter a wrong url
@app.errorhandler(404) 
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('errors/404.html'), 404

@app.errorhandler(403) 
def error_403(error):
    return render_template('/errors/403.html'), 403

@app.errorhandler(500) 
def error_500(error):
    return render_template('/errors/500.html'), 500
