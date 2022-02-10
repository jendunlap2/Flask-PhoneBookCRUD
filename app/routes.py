from app import app, db
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.forms import RegisterForm, LoginForm, AddressForm
from app.models import User, Address

@app.route('/')
def index():
    addresses = Address.query.all()
    return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Get data from the form 
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        # Check if either the username or email is already in db
        user_exists = User.query.filter((User.username == username)|(User.email == email)).all()
        
        # If so, return back to register page
        if user_exists:
            flash(f"User with username {username} or email {email} already exists", "danger")
            return redirect(url_for('register'))
        
        # Create a new user instance using form
        User(username=username, email=email, password=password)
        flash("Thank you for registering!", "primary")
        return redirect(url_for('index'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Get the data from the form
        username = form.username.data
        password = form.password.data
        
        # Query user table for user with username
        user = User.query.filter_by(username=username).first()
        
        # If user does not exist or used incorrect password
        if not user or not user.check_password(password):
            
            # redirect to login page
            flash('Username or password is incorrect', 'danger')
            return redirect(url_for('login'))
        
        # if user does exist and correct password, log user in
        login_user(user)
        flash('You have succesfully logged in', 'success')
        return redirect(url_for('index'))
        
        
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out.", "warning")
    return redirect(url_for('index'))
    
@app.route('/addresses')
def address_info(address_id):
    address = Address.query.get_or_404(address_id)
    return render_template('address.html', address=address)

@app.route('/addresses', methods=["GET", "POST"])
@login_required
def edit_address(address_id):
    address = Address.query.get_or_404(address_id)
    form = AddressForm()
    if form.validate_on_submit():
        name = form.name.data
        street = form.street.data
        city = form.city.data
        state = form.state.data
        zip_code = form.zip_code.data
        
        address.name = name
        address.street = street
        address.city = city
        address.state = state
        address.zip_code = zip_code
        
        address.save()
        
        flash(f"{address.name} has been updated.", "primary")
        return redirect(url_for('address_info', address_id=address.id))
        
    return render_template('edit_address.html', address=address, form=form)

@app.route('/addresses/delete')
@login_required
def delete_address(address_id):
    address = Address.query.get_or_404(address_id)
    address.delete()
    flash(f"{address.name} address has been deleted.", 'danger')
    return redirect(url_for('index'))


@app.route('/add_address', methods=["GET", "POST"])
@login_required
def add_address():
    form = AddressForm()
    if form.validate_on_submit():
        # Get the data from the form
        name = form.name.data
        street = form.street.data
        city = form.city.data
        state = form.state.data
        zip_code = form.zip_code.data
        
        # Check if either the name or address is already in db
        address_exists = Address.query.filter((Address.name == name)|(Address.street == street)).all()
        
        # If so, return back to add_address page
        if address_exists:
            flash(f"Address with name: {name} or address: {street} already exists", "danger")
            return redirect(url_for('add_address'))
        
        # Create a new address instance using form
        Address(name=name, street=street, city=city, state=state, zip_code=zip_code)
        flash("Address has been added.", "primary")
        return redirect(url_for('index'))
    
    return render_template('add_address.html', form=form)