from decimal import Decimal

from flask import render_template, request, redirect, url_for, flash, Response, send_file, current_app
from app import app, engine, db
from app.forms import LoginForm, RegistrationForm, PayBillForm
from app.models import Borough, Development, Building, Bills, Users
from functools import wraps
from flask_login import login_user, current_user, logout_user, login_required
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import bcrypt

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


#%%
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        dev_id = Users.query.filter_by(username = current_user.username).first().dev_id
        if dev_id == 0:
            return render_template('main.html', id=str(dev_id), visible=1)
        return redirect(url_for('buildings', id=str(dev_id)))
    form = LoginForm()
    if form.validate_on_submit():
        userlogin = form.username.data.lower().strip()
        user = Users.query.filter_by(username = userlogin).first()
        print(user)
        if user and form.password.data == user.password:
            login_user(user, remember=form.remember.data)
            # user.authenticated = True
            dev_id = user.dev_id
            if dev_id == 0:
                return render_template('main.html', id=str(dev_id), visible=1)
            return redirect(url_for('buildings', id = str(dev_id)))
        else:
            flash('Login Unsuccessful. Please check your username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

#%%
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # query = f"INSERT into users VALUES('{form.username.data.lower().strip()}',{form.dev.data},'{form.password.data}')"
        # with engine.begin() as conn:  # TRANSACTION
        #     conn.execute(query)
        #     conn.execute("COMMIT")
        user = Users(username=form.username.data.lower().strip(), password=form.password.data, dev_id = form.dev.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route('/list_dev/<borough>')
@login_required
def list_dev(borough):
    borough_id=0
    if int(borough) == 0:
        dev = Development.query.all()
        borough_name = "ALL BOROUGHS"
    else:
        dev = Development.query.filter_by(borough_id=int(borough)).all()
        print(dev[0].borough.name)
        borough_name = dev[0].borough.name
        borough_id = dev[0].borough_id
    return render_template('dev.html', dev=dev, borough_name=borough_name, borough_id=borough_id)

@app.route('/buildings/<id>')
@login_required
def buildings(id):
    dev_name = None
    print('current user', current_user)
    borough_name = "borough_name"
    borough = 0
    if id[0] == 'b':
        borough = int(id[1])
        if borough == 0:
            bldg = Building.query.all()
            borough_name = "ALL BOROUGHS"
        else:
            bldg = Building.query.join(Development, Building.dev_id == Development.dev_id).filter_by(borough_id=borough)
            borough_name = bldg[0].dev.borough.name
    else:
        bldg = Building.query.join(Development, Building.dev_id == Development.dev_id).filter_by(dev_id=int(id))
        dev_name = bldg[0].dev.name
        borough_name = bldg[0].dev.borough.name
        borough = bldg[0].dev.borough_id
    return render_template('buildings.html', bldg=bldg, borough_name=borough_name, dev_name=dev_name, borough='b'+str(borough), borough_id=borough)

@app.route('/charges/<bldg_id>')
@login_required
def charges(bldg_id):
    try:
        bills = Bills.query.filter_by(building_id=int(bldg_id)).all()
        borough_name = bills[0].building.dev.borough.name
        borough_id = bills[0].building.dev.borough_id
        dev_id = bills[0].building.dev.dev_id
        dev_name = bills[0].building.dev.name
        bldg_name = bills[0].building.location
    except Exception as e:
        building = Building.query.filter_by(building_id=int(bldg_id)).first()
        borough_name = building.dev.borough.name
        borough_id = building.dev.borough_id
        dev_id = building.dev.dev_id
        dev_name = building.dev.name
        bldg_name = building.location
        output = f"Development: {dev_name} Building: {bldg_name} Building ID: {bldg_id} had no charges from 2018-2020. <br> Due to space constraints of 10K records on Heroku server for free accounts, I eliminated charges prior to 2018 from the database."
        return output + "<p>Error for debugging purposes only: " + str(e)

    return render_template('charges.html', bldg_id=bldg_id, bills=bills, borough_name=borough_name, dev_name=dev_name, bldg_name=bldg_name, borough_id=borough_id, dev_id=dev_id)

#%%
@app.route("/delete/<bill_id>/<bldg_id>")
@login_required
def delete(bill_id, bldg_id):
    Bills.query.filter_by(bill_id=bill_id).delete()
    db.session.commit()
    flash(f'Bill#{bill_id} was successfully deleted.', 'success')
    return redirect(url_for('charges', bldg_id=bldg_id))


#%%
@app.route("/edit/<bill_id>/<bldg_id>/<amount>")
@login_required
def edit(bill_id, bldg_id, amount):
    Bills.query.filter_by(bill_id=int(bill_id)).first().current_charges = float(amount)
    db.session.commit()
    flash(f'Bill#{bill_id} was successfully edited with new amount ${float(amount):.2f}', 'success')
    return redirect(url_for('charges', bldg_id=bldg_id))



#%%
@app.route("/pay_bill", methods=['GET', 'POST'])
@login_required
def pay_bill():
    # if current_user.is_authenticated:
    #     return redirect(url_for('buildings', id=str(6)))
    form = PayBillForm()
    if form.validate_on_submit():
        amount = form.amount.data
        return render_template('confirmation.html', amount=amount)
    # else:
    #     flash('Payment Unsuccessful. Please check your credit card number.', 'danger')
    return render_template('pay_bill.html', title='Pay Bill', form=form)

@app.route('/pdf')
def pdf():
    return send_file('static/resources/documentation.pdf', attachment_filename='documentation.pdf')

