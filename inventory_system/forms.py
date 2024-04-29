from flask_wtf import FlaskForm # pip install flask-wtf
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo,ValidationError
from flask_wtf.file import FileField,FileAllowed
from inventory_system.models import User,Product,Sale


from inventory_system import current_user,ALLOWD_EXTENSIONS

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWD_EXTENSIONS

# form for profile
class UpdateProfileForm(FlaskForm): 
    fname=StringField('Full Name',validators=[DataRequired(),Length(min=3, max=30)],render_kw={'placeholder' :'Enter Full Name'})
    email=StringField('Email',validators=[DataRequired(),Email()],render_kw={'placeholder' :'Enter Email'}) # pip install email_validator
    bio = TextAreaField('Bio')
    picture = FileField(
        "Update Profile Picture", validators=[FileAllowed(ALLOWD_EXTENSIONS)]
    )
    submit = SubmitField("Update")

    # def validate_username(self, username):
    #     user = Users.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError('Username already exists! Please chosse a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists! Please chosse a different one')



# form for Sign Up 
class RegistrationForm(FlaskForm): 
    fname=StringField('Full Name',validators=[DataRequired(),Length(min=3, max=30)],render_kw={'placeholder' :'Enter Full Name'})
    email=StringField('Email',validators=[DataRequired(),Email()],render_kw={'placeholder' :'Enter Email'}) # pip install email_validator
    password= PasswordField('Password',validators=[DataRequired(),Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,32}$")],render_kw={'placeholder' :'Enter Password'})
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")],render_kw={'placeholder' :'Confirm Password'})
    submit = SubmitField("Sign Up")

    # def validate_username(self, username):
    #     user = Users.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError('Username already exists! Please chosse a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists! Please chosse a different one')


# form for login 
class LoginForm(FlaskForm): 
    email = StringField("Email", validators=[DataRequired(), Email()],render_kw={'placeholder' :'Enter Email'})
    password = PasswordField( "Password",validators=[ DataRequired(),],render_kw={'placeholder' :'Enter Password'}
    )
    remember = BooleanField("Remember Me") 
    submit = SubmitField("Log In")




# form for Reset Password   
class RequestResetForm(FlaskForm): # This form used to let the user to request to reset his password
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm): # This form used to let the user to reset his password
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Regexp(
                "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,32}$"
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")

