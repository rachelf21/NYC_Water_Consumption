from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import app, db
from sqlalchemy.exc import IntegrityError




class Borough(db.Model):
    __tablename__ = 'borough'
    __table_args__ = {'extend_existing': True}
    borough_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, id, name):
        self.borough_id = id
        self.name = name

    def __repr__(self):
        return f"Borough: ('{self.borough_id}', '{self.name}')"


class Development(db.Model):
    __tablename__ = 'development'
    __table_args__ = {'extend_existing': True}
    dev_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    borough_id = db.Column(db.Integer, db.ForeignKey('borough.borough_id'), nullable=False)
    borough = db.relationship('Borough', backref='borough', lazy=True)
    tds = db.Column(db.Integer, nullable=False)
    edp = db.Column(db.Integer, nullable=False)
    amp = db.Column(db.String(20))
    funding_source = db.Column(db.String(50))

    def __init__(self, id, name):
        self.dev_id = id
        self.name = name

    def __repr__(self):
        return f"Development: ('{self.dev_id}', '{self.name}') , '{self.borough.name}"

class Building(db.Model):
    __tablename__ = 'building'
    __table_args__ = {'extend_existing': True}
    building_id = db.Column(db.Integer, primary_key=True, nullable=False)
    dev_id = db.Column(db.Integer, db.ForeignKey("development.dev_id"), nullable=False)
    dev = db.relationship('Development', backref='dev', lazy=True)
    location = db.Column(db.String(50))
    rc_code = db.Column(db.String(20), nullable=False)
    def __repr__(self):
        return f"Building: ('dev_id:{self.dev_id}', 'building_id:{self.building_id}', '{self.location}')"

class Meter(db.Model):
    __tablename__ = 'meter'
    __table_args__ = {'extend_existing': True}
    meter_id = db.Column(db.Integer, primary_key=True, nullable=False)
    meter_type = db.Column(db.String(10))
    scope = db.Column(db.String(50))
    meter_number = db.Column(db.String(20), nullable=False)

class Vendor(db.Model):
    __tablename__ = 'vendor'
    __table_args__ = {'extend_existing': True}
    vendor_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50))

class Rate(db.Model):
    __tablename__ = 'rate'
    __table_args__ = {'extend_existing': True}
    rate_id = db.Column(db.Integer, primary_key=True, nullable=False)
    rate_class = db.Column(db.String(50))

class Bill(db.Model):
    __tablename__ = 'bill'
    __table_args__ = {'extend_existing': True }
    bill_id = db.Column('bill_id', db.Integer, primary_key=True)
    umis_bill_id = db.Column('umis_bill_id', db.String(20))
    building_id = db.Column('building_id', db.Integer, db.ForeignKey("building.building_id"), nullable=False)
    building = db.relationship('Building', backref='building', lazy=True)
    meter_id = db.Column('meter_id', db.Integer, db.ForeignKey("meter.meter_id"), nullable=False)
    meter = db.relationship('Meter', backref='meter', lazy=True)
    vendor_id = db.Column('vendor_id', db.Integer, db.ForeignKey("vendor.vendor_id"), nullable=False)
    vendor = db.relationship('Vendor', backref='vendor', lazy=True)
    rate_id = db.Column('rate_id', db.Integer, db.ForeignKey("rate.rate_id"), nullable=False)
    rate = db.relationship('Rate', backref='rate', lazy=True)
    revenue_month = db.Column('revenue_month', db.String(20), nullable=False)
    service_start_date = db.Column('service_start_date', db.Date, nullable=False)
    service_end_date = db.Column('service_end_date', db.Date, nullable=False)
    days = db.Column('days', db.Integer, nullable=False)
    estimated = db.Column('estimated', db.Boolean, nullable=False)
    current_charges = db.Column('current_charges', db.Numeric, nullable=False)
    bill_analyzed = db.Column('bill_analyzed', db.String(10), nullable=False)
    consumption = db.Column('consumption', db.Integer, nullable=False)
    water_and_sewer_charges = db.Column('water_and_sewer_charges', db.Numeric, nullable=False)
    other_charges = db.Column('other_charges', db.Numeric, nullable=False)