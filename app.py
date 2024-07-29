from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import CSRFProtect
import pickle
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# CSRF protection
csrf = CSRFProtect(app)

# Load data using pickle (replace file names with your actual pickle files)
with open('popular.pkl', 'rb') as f:
    popular_df = pickle.load(f)

with open('pt.pkl', 'rb') as f:
    pt = pickle.load(f)

with open('books.pkl', 'rb') as f:
    books = pickle.load(f)

with open('similarity_scores.pkl', 'rb') as f:
    similarity_scores = pickle.load(f)

# SQLAlchemy setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Define LoginForm using Flask-WTF
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Define RegisterForm using Flask-WTF
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

# Routes for your application
@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating = [round(r, 2) for r in popular_df['avg_rating'].values]
                           )

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    form = LoginForm()  # Instantiate the LoginForm here

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Query the database to find the user
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            # Set session variables upon successful login
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))  # Redirect to index or another appropriate page
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('recommend.html', form=form)

@app.route('/recommend_books', methods=['POST'])
def recommend_books():
    user_input = request.form.get('user_input')

    # Recommendation logic (example using books DataFrame)
    temp_df_title = books[books['Book-Title'].str.contains(user_input, case=False, na=False)]
    temp_df_author = books[books['Book-Author'].str.contains(user_input, case=False, na=False)]

    if temp_df_title.empty and temp_df_author.empty:
        return render_template('error.html', message='No books found matching your search. Please try another query.')

    combined_df = pd.concat([temp_df_title, temp_df_author]).drop_duplicates(subset='Book-Title')
    data = []
    for index, row in combined_df.iterrows():
        item = [row['Book-Title'], row['Book-Author'], row['Image-URL-M']]
        data.append(item)

    return render_template('recommend.html', form=LoginForm(), data=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Create an instance of the LoginForm

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Query the database to find the user
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            # Set session variables upon successful login
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()  # Create an instance of RegisterForm

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Check if the username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

        if existing_user:
            flash('Username or email already exists. Please choose a different one.', 'danger')
        else:
            # Create a new user and add to the database
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/logout', methods=['POST'])
def logout():
    # Check if the user is logged in before logging out
    if 'username' in session:
        # Clear session variables to log out the user
        session.pop('username', None)
        flash('You have been logged out.', 'info')

    # Redirect to the index page after logout
    return redirect(url_for('index'))

@app.route('/my_account')
def my_account():
    # Add logic here to fetch user-specific data or render the my_account template
    return render_template('my_account.html')

if __name__ == '__main__':
    app.run(debug=True)
