from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, Blueprint
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import random
import mysql.connector
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db, Car, User
from recommendation import recommend_products
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField, EmailField, BooleanField
from wtforms.validators import DataRequired, Email





app = Flask(__name__)
app.secret_key = 'eb965420ec0aa9b092cc052672008a776031707773902239bc5960ad1edfaeb9'
csrf = CSRFProtect(app)


# Configure MySQL connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Afham.my0799',
    'database': 'car_recommendation'
}

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Afham.my0799@localhost/car_recommendation'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Load data from CSV
def load_data():
    df = pd.read_csv('C:/fyp/cars.csv')
    return df

# Define forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    show_password = BooleanField('Show Password')
    submit = SubmitField('Register')

class FindCarForm(FlaskForm):
    min_wage = StringField('Minimum Wage', validators=[DataRequired()])
    loan_term_years = StringField('Loan Term (years)', validators=[DataRequired()])
    coverage_type = StringField('Coverage Type', validators=[DataRequired()])
    ncd = StringField('NCD', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = StringField('Your Email', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired()])
    show_password = BooleanField('Show Password')
    submit = SubmitField('Change Password')



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# Routes
@app.route('/', methods=['GET', 'POST'])
def home():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data
        # Process the form data (e.g., send an email, save to database)
        flash('Your message has been sent. Thank you!')
        return jsonify({'status': 'success'})
    else:
        recommended_cars = Car.query.all()
        random_cars = random.sample(recommended_cars, 6)
        return render_template('index.html', recommended_cars=random_cars, form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    user = current_user
    recommended_cars = Car.query.all()
    random_cars = random.sample(recommended_cars, 6)
    
    form = ContactForm()  # Ensure form is defined and passed to template
    
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data
        
        # Handle the form submission (e.g., save to database, send email)
        
        # Return JSON response indicating success
        return jsonify(status='success')
    
    # Render the template with the form
    return render_template('dashboard.html', user=user, recommended_cars=random_cars, form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        hashed_password = generate_password_hash(password, method='scrypt')

        # Create a new user instance
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user is None:
            return jsonify({'message': 'You are not registered', 'category': 'danger'}), 404

        if not check_password_hash(user.password, password):
            return jsonify({'message': 'Wrong password', 'category': 'danger'}), 401

        login_user(user)
        return jsonify({'message': 'Login successful', 'category': 'success'}), 200
    
    return render_template('login.html', form=form)

@app.route('/find_car', methods=['GET', 'POST'])
@login_required
def find_car():
    user = current_user

    form = FindCarForm()
    if form.validate_on_submit():
        min_wage = float(form.min_wage.data)
        loan_term_years = int(form.loan_term_years.data)
        coverage_type = form.coverage_type.data
        ncd = form.ncd.data

        # Load car data from the database
        cars_query = Car.query.all()
        cars_data = pd.DataFrame([car.to_dict() for car in cars_query])

        # Get the search brand from the form
        search_brand = request.form.get('brand', '').strip()

        # Define filters with only the brand search
        filters = {
            'brand': search_brand
        }

        # Recommend products based on the provided logic
        recommended_cars_df, details = recommend_products(
            min_wage, loan_term_years, coverage_type, ncd, filters, cars_data
        )

        # Convert DataFrame to a list of dictionaries for rendering
        recommended_cars_list = recommended_cars_df.to_dict(orient='records')

        # Format details to two decimal places, except for 'num_affordable_products'
        for key in details:
            if key == 'num_affordable_products':
                details[key] = int(details[key])  # No decimal places
            else:
                details[key] = f"{details[key]:.2f}"  # Two decimal places

        return render_template('find_car.html', form=form, recommended_cars=recommended_cars_list, details=details, user=user)

    return render_template('find_car.html', form=form, user=user)


@app.route('/autocomplete_brands')
def autocomplete_brands():
    query = request.args.get('query', '').lower()
    brands = Car.query.with_entities(Car.brand).distinct()
    matching_brands = [brand for (brand,) in brands if query in brand.lower()]
    return jsonify(matching_brands)


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


@app.route('/favorite')
@login_required
def favorite():
    user = current_user
    favorite_cars = user.favorite_cars
    return render_template('favorite.html', favorite_cars=favorite_cars, user=user)

@app.route('/cars')
def display_cars():
    cars = Car.query.all()
    return render_template('cars.html', cars=cars)

@app.route('/popup_message')
def popup_message():
    message = "Please log in to save your progress."
    return jsonify(message=message)

@app.route('/add_to_favorites', methods=['POST'])
@login_required
def add_to_favorites():
    data = request.get_json()
    car_id = data.get('car_id')
    
    if not car_id:
        return jsonify({'message': 'Car ID is required'}), 400

    car = Car.query.get(car_id)
    if not car:
        return jsonify({'message': 'Car not found'}), 404

    if car not in current_user.favorite_cars:
        current_user.favorite_cars.append(car)
        db.session.commit()
        return jsonify({'message': 'Car added to favorites!'})
    else:
        return jsonify({'message': 'Car is already in favorites.'})
    
@app.route('/remove_favorite/<int:car_id>', methods=['POST'])
@login_required
def remove_favorite(car_id):
    car = Car.query.get_or_404(car_id)
    if car in current_user.favorite_cars:
        current_user.favorite_cars.remove(car)
        db.session.commit()
        flash('Car removed from favorites!', 'success')
    else:
        flash('Car not found in favorites.', 'warning')
    return redirect(url_for('favorite'))

@app.route('/is_logged_in')
def is_logged_in():
    if current_user.is_authenticated:
        return jsonify(logged_in=True)
    return jsonify(logged_in=False)

@app.route('/profile')
@login_required
def profile():
    user = User.query.get(current_user.id)
    
    if user:
        user_data = {
            'id': user.id,
            'username': user.username,
        }
        return render_template('profile.html', user_data=user_data, user=current_user)
    else:
        return jsonify({'message': 'User not found'}), 404
    
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user
    form = EditProfileForm()
    if form.validate_on_submit():
        # Update the current user's username
        current_user.username = form.username.data
        db.session.commit()
        
        # Flash a success message
        flash('Username updated successfully!', 'Username updated successfully!')
        return redirect(url_for('edit_profile'))
    
    # Render the template with the form and current user
    return render_template('edit_profile.html', form=form, user=user)

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    user = current_user
    form = ChangePasswordForm()

    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data

        if not check_password_hash(user.password, current_password):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('change_password'))

        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            return redirect(url_for('change_password'))

        hashed_password = generate_password_hash(new_password, method='scrypt')
        user.password = hashed_password
        db.session.commit()
        flash('Password changed successfully!', 'Password changed successfully!')
        return redirect(url_for('profile'))

    return render_template('change_password.html', form=form, user=user)




@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = User.query.get(current_user.id)
    
    if user:
        db.session.delete(user)
        db.session.commit()
        logout_user()
        return redirect(url_for('home'))
    else:
        return jsonify({'message': 'User not found'}), 404

    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('username', None)
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)