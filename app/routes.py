from flask import render_template, request, Response
from app import app
from app.models import Borough, Development, Building, Bill

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/list_dev/<borough>')
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
def buildings(id):
    dev_name = None
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
def charges(bldg_id):
    try:
        bills = Bill.query.filter_by(building_id=int(bldg_id)).all()
        borough_name = bills[0].building.dev.borough.name
        borough_id = bills[0].building.dev.borough_id
        dev_id = bills[0].building.dev.dev_id
        dev_name = bills[0].building.dev.name
        bldg_name = bills[0].building.location
    except Exception as e:
        return "Not available at this time " + str(e)

    return render_template('charges.html', bills=bills, borough_name=borough_name, dev_name=dev_name, bldg_name=bldg_name, borough_id=borough_id, dev_id=dev_id)