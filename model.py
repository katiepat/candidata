
from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


#Model definitions


class Candidate_Summary(db.Model):
    """Candidate summary class """    


    __tablename__ = 'candidate_summaries'

    cand_summary_id = db.Column(db.String(100), nullable=False, primary_key=True)

    cid = db.Column(db.String(100), db.ForeignKey('candidates.cid'), nullable=False)
    cand_name = db.Column(db.String(250), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    chamber = db.Column(db.String(100), nullable=False)
    first_elected = db.Column(db.String(100), nullable=True)
    total = db.Column(db.Integer, nullable=False)
    spent = db.Column(db.Integer, nullable=False)
    cash_on_hand = db.Column(db.Integer, nullable=False)
    debt = db.Column(db.Integer, nullable=False)




class Candidate(db.Model):
    """Candidate on website """

    __tablename__ = 'candidates'


    cid = db.Column(db.String(100), nullable=False, primary_key=True)
    district_id = db.Column(db.String(100), nullable=False)
    party_id = db.Column(db.String(50), nullable=False)
    cand_summary_id =db.Column(db.String(100),
                    db.ForeignKey('candidate_summaries.cand_summary_id'), 
                    nullable=False)
    top_industries = db.Column(db.String(100), 
                    db.ForeignKey('candidate_industries.candidate_industry_id'), 
                    nullable=False)
    top_organizations = db.Column(db.String(100), 
                        db.ForeignKey('candidate_organizations.candidate_org_id'),
                        nullable=False)





class Candidate_Industry(db.Model):



    __tablename__ = "candidate_industries"

    candidate_industry_id = db.Column(db.String(100), nullable=False, primary_key=True)
    
    cid = db.Column(db.String(100), db.ForeignKey('candidates.cid'), nullable=False)
    industry_id = db.Column(db.String(100), db.ForeignKey('industries.industry_id'), nullable=False)

    total = db.Column(db.Integer, nullable=False)
    total_from_indivs = db.Column(db.Integer, nullable=True)
    total_from_pacs =db.Column(db.Integer, nullable=True)

    candidate = db.relationship('Candidate', backref=db.backref('candidate_industries', order_by=candidate_industry_id))

    industry = db.relationship('Industry', backref=db.backref('candidate_industries', order_by=candidate_industry_id))



class Industry(db.Model):
    """Industry information """

    __tablename__ = 'industries'


    industry_id = db.Column(db.String(100), nullable=False, primary_key=True)
    industry_name = db.Column(db.String(100), nullable=False)


class Organization(db.Model):
    """Organization on website"""

    __tablename__ = 'organizations'

    #use org id from CRP
    org_summary_id = db.Column(db.String(50), nullable=False, primary_key=True)
    

    org_name = db.Column(db.String(200), nullable=False)
    #number of members invested in organization (int)
    num_members_invested = db.Column(db.Integer, nullable=False)

    #total contributions (int)
    total = db.Column(db.Integer, nullable=False)

    #total from organization's PAC
    total_from_org_pac = db.Column(db.Integer, nullable=True)

    #total from individuals
    total_from_indivs = db.Column(db.Integer, nullable=True)

    #total soft money
    total_soft_money = db.Column(db.Integer, nullable=True)

    #total money coming from 527
    total_from_527 = db.Column(db.Integer, nullable=True)

    #total to democratic candidates and party committees
    total_to_dems = db.Column(db.Integer, nullable=True)

    #total to republican candidates and party committees
    total_to_repubs = db.Column(db.Integer, nullable=True) 

    #total lobbying money for two years of cycle
    total_spent_on_lobbying = db.Column(db.Integer, nullable=True)

    #total amount spent on independent expenditures
    total_spent_on_outside_money = db.Column(db.Integer, nullable=True) 

    #total given to PACs
    gave_to_pac = db.Column(db.Integer, nullable=True)

    #total given to 527 organizations
    gave_to_527 = db.Column(db.Integer, nullable=True)

    #total given to candidates
    gave_to_cand = db.Column(db.Integer, nullable=True)

    #total given to party committees"
    gave_to_party = db.Column(db.Integer, nullable=True)




class Candidate_Organization(db.Model):
    """ """
    __tablename__ = 'candidate_organizations'

    candidate_org_id = db.Column(db.String(100), nullable=False, primary_key=True)
    
    cid = db.Column(db.String(100), db.ForeignKey('candidates.cid'), nullable=False)
    org_id = db.Column(db.String(100), db.ForeignKey('organizations.org_summary_id'), nullable=False)
    total = db.Column(db.Integer, nullable=False)
    pacs = db.Column(db.Integer, nullable=False)

    candidate = db.relationship('Candidate', backref=db.backref('candidate_organizations', order_by=candidate_org_id))

    organization = db.relationship('Organization', backref=db.backref('candidate_organizations', order_by=candidate_org_id))











#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///campaign_finance_tracker'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")