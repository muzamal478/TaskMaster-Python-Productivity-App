from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(2, 80)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class TaskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(1,140)])
    description = TextAreaField("Description", validators=[Optional()])
    category = StringField("Category", validators=[Optional(), Length(max=60)])
    priority = SelectField("Priority", choices=[("Low","Low"),("Medium","Medium"),("High","High"),("Urgent","Urgent")], default="Medium")
    due_date = StringField("Due Date (YYYY-MM-DD HH:MM)", validators=[Optional()])
    reminder = BooleanField("Enable reminder")
    submit = SubmitField("Save")
