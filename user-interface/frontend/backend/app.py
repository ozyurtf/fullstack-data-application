from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify
from flask_cors import CORS
import logging

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customer'
    
    customerssn = db.Column(db.String(11), primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    emailaddress = db.Column(db.String(100))
    phone = db.Column(db.String(12))

    # accounts = db.relationship('Account', back_populates='customer')

    def to_dict(self):
        return {
            'customerssn': self.customerssn,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'emailaddress': self.emailaddress,
            'phone': self.phone
        }

class Account(db.Model):
    __tablename__ = 'account'
    
    acctnumber = db.Column(db.String(50), primary_key=True)
    customerssn = db.Column(db.String(11), db.ForeignKey('customer.customerssn'))
    nomonthsinactive = db.Column(db.Integer)
    activitystatus = db.Column(db.String(30))
    activitystatusdate = db.Column(db.Date)
    accountestablisheddate = db.Column(db.Date)

    # customer = db.relationship('Customer', back_populates='accounts')

    def to_dict(self):
        return {
            'acctnumber': self.acctnumber,
            'customerssn': self.customerssn,
            'nomonthsinactive': self.nomonthsinactive,
            'activitystatus': self.activitystatus,
            'activitystatusdate': str(self.activitystatusdate),
            'accountestablisheddate': str(self.accountestablisheddate)
        }
    
class LastInvoiceDetailPerCustomer(db.Model):
    __tablename__ = 'lastinvoicedetailspercustomer'
    
    customerssn = db.Column(db.String(11), primary_key=True)
    lastinvoicedate = db.Column(db.Date)
    duedate = db.Column(db.Date)
    paiddate = db.Column(db.Date)
    invoicestatus = db.Column(db.String(20)) 
    nooutstandinginvoices = db.Column(db.Integer)

    # customer = db.relationship('Customer', back_populates='accounts')

    def to_dict(self):
        return {
            'lastinvoicedate': self.lastinvoicedate.isoformat() if self.lastinvoicedate else None,
            'duedate': self.duedate.isoformat() if self.duedate else None,
            'paiddate': self.paiddate.isoformat() if self.paiddate else None,
            'invoicestatus': self.invoicestatus,
            'nooutstandinginvoices': str(self.nooutstandinginvoices)
        }    

class CustomerContract(db.Model):
    __tablename__ = 'customercontract'
    
    customerssn = db.Column(db.String(11), db.ForeignKey('customer.customerssn'), primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    phone = db.Column(db.String(12))
    state = db.Column(db.String(50))
    contractnumber = db.Column(db.String(50), primary_key=True)
    contracttype = db.Column(db.String(10))
    effectivedate = db.Column(db.Date)
    expirationdate = db.Column(db.Date)
    renewaldate = db.Column(db.Date)
    policyid = db.Column(db.String(50))
    premiumcode = db.Column(db.String(50), primary_key=True)
    premiumamount = db.Column(db.Float)
    premiumfrequency = db.Column(db.String(20))
    premiumamountincreaserate = db.Column(db.Float)
    newpremiumamount = db.Column(db.Float)

    __table_args__ = (
        db.PrimaryKeyConstraint('customerssn', 'contractnumber', 'premiumcode'),
    )


    def to_dict(self):
        return {
            'contractnumber': self.contractnumber,
            'contracttype': self.contracttype,
            'effectivedate': self.effectivedate.isoformat() if self.effectivedate else None,
            'expirationdate': self.expirationdate.isoformat() if self.expirationdate else None,
            'renewaldate': str(self.renewaldate),
            'policyid': self.policyid,
            'premiumamount': self.premiumamount,
            'premiumfrequency': self.premiumfrequency,
            'newpremiumamount': self.newpremiumamount,
        }    

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})

logging.basicConfig(level=logging.DEBUG)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:secretpassword@localhost/postgres'
db.init_app(app)

@app.route('/api/customerssn/<string:customerssn>', methods=['GET'])
def get_customer_info(customerssn):
    app.logger.info(f"Received request for Customer SSN: {customerssn}")
    try:
        customer = Customer.query.get(customerssn)

        if customer:
            account = Account.query.filter_by(customerssn = customerssn).first()
            lastinvoicedetailpercustomer = LastInvoiceDetailPerCustomer.query.filter_by(customerssn = customerssn).first()
            customercontract = CustomerContract.query.filter_by(customerssn = customerssn).first()
            data = {
                'customer': customer.to_dict(),
                'account': account.to_dict() if account else None,
                'lastinvoicedetailpercustomer': lastinvoicedetailpercustomer.to_dict() if lastinvoicedetailpercustomer else None,
                'customercontract': customercontract.to_dict() if customercontract else None
            }
            app.logger.info(f"Returning data for Customer SSN {customerssn}: {data}")
            return jsonify(data), 200
        
        app.logger.info(f"Customer SSN {customerssn} not found")
        return jsonify({'error': 'Customer not found'}), 404
    
    except Exception as e:
        app.logger.error(f"Error processing request for Customer SSN {customerssn}: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/')
def home():
    return "Customer API is running. Use /api/customerssn/<ssn> to get Customer and Account information."

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)