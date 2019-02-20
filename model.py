
from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


#Model definitions





class Candidate_Summary(db.Model):
    """Financial summary information for specific candidate"""    


    __tablename__ = 'candidate_summaries'

    cand_summary_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)

    cid = db.Column(db.String(100), db.ForeignKey('candidates.cid'), nullable=False)
  
    state = db.Column(db.String(20), nullable=False)
    chamber = db.Column(db.String(100), nullable=True)
    first_elected = db.Column(db.String(100), nullable=True)
    total = db.Column(db.Float(), nullable=True)
    spent = db.Column(db.Float(), nullable=True)
    cash_on_hand = db.Column(db.Float(), nullable=True)
    debt = db.Column(db.Float(), nullable=True)

    candidate = db.relationship('Candidate', foreign_keys=[cid])





class Industry(db.Model):
    """ Industry """

    __tablename__ = 'industries'


    industry_id = db.Column(db.String(100), nullable=False, primary_key=True)
    industry_name = db.Column(db.String(100), nullable=False)


    
    candidate_industries = db.relationship('Candidate_Industry')
    
    # candidate = db.relationship('Candidate', secondary='candidate_industry', backref='industries')

class Candidate_Industry(db.Model):
    """ Top industry contributions for specific candidate"""
    """ Middle Table"""


    __tablename__ = 'candidate_industries'

    candidate_industry_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    
    cid = db.Column(db.String(100), db.ForeignKey('candidates.cid'), nullable=True)
    industry_id = db.Column(db.String(100), db.ForeignKey('industries.industry_id'), nullable=True)
    total = db.Column(db.Float(), nullable=True)
    total_from_indivs = db.Column(db.Float(), nullable=True)
    total_from_pacs =db.Column(db.Float(), nullable=True)

    

    candidate = db.relationship('Candidate', foreign_keys=[cid])

    industry = db.relationship('Industry', foreign_keys=[industry_id])



class Candidate(db.Model):
    """Candidate """
    """ Middle Table """

    __tablename__ = 'candidates'


    cid = db.Column(db.String(100), nullable=False, primary_key=True)
    cand_name = db.Column(db.String(250), nullable=False)
    party_id = db.Column(db.String(50), nullable=False)
    district_id = db.Column(db.String(100), nullable=False)
    
    cand_summary_id = db.Column(db.Integer, 
                    db.ForeignKey('candidate_summaries.cand_summary_id'), 
                    nullable=True)
                 
    top_industries = db.Column(db.Integer,
                    db.ForeignKey('candidate_industries.candidate_industry_id'), 
                    nullable=True)
                    
    top_organizations = db.Column(db.Integer, 
                        db.ForeignKey('candidate_organizations.candidate_org_id'), 
                        nullable=True)
                       
    


    cand_industries = db.relationship('Candidate_Industry', foreign_keys=[candidate_industry_id])
    # industries = db.relationship('Industry', secondary='candidate_industries', backref='candidates')
    summary = db.relationship('Candidate_Summary', foreign_keys=[cand_summary_id])
    
    cand_orgs = db.relationship('Candidate_Organization', foreign_keys=[candidate_org_id])
    # organizations = db.relationship('Organization', secondary='candidate_organizations', backref='candidates')    


class Organization(db.Model):
    """ Organization """

    __tablename__ = 'organizations'

    #use org id from CRP
    org_summary_id = db.Column(db.String(50), nullable=False, primary_key=True)
    

    org_name = db.Column(db.String(200), nullable=False)
    #number of members invested in organization (int)
    num_members_invested = db.Column(db.Integer, nullable=False)

    #total contributions (int)
    total = db.Column(db.Float(), nullable=False)

    #total from organization's PAC
    total_from_org_pac = db.Column(db.Float(), nullable=True)

    #total from individuals
    total_from_indivs = db.Column(db.Float(), nullable=True)

    #total soft money
    total_soft_money = db.Column(db.Float(), nullable=True)

    #total money coming from 527
    total_from_527 = db.Column(db.Float(), nullable=True)

    #total to democratic candidates and party committees
    total_to_dems = db.Column(db.Float(), nullable=True)

    #total to republican candidates and party committees
    total_to_repubs = db.Column(db.Float(), nullable=True) 

    #total lobbying money for two years of cycle
    total_spent_on_lobbying = db.Column(db.Float(), nullable=True)

    #total amount spent on independent expenditures
    total_spent_on_outside_money = db.Column(db.Float(), nullable=True) 

    #total given to PACs
    gave_to_pac = db.Column(db.Float(), nullable=True)

    #total given to 527 organizations
    gave_to_527 = db.Column(db.Float(), nullable=True)

    #total given to candidates
    gave_to_cand = db.Column(db.Float(), nullable=True)

    #total given to party committees"
    gave_to_party = db.Column(db.Float(), nullable=True)


    cand_orgs = db.relationship('Candidate_Organization')
    # candidates = db.relationship('Candidate', secondary='candidate_organizations', backref='organizations' )





class Candidate_Organization(db.Model):
    """ Top Organizations for Specific Candidate """
    """ Middle Table"""



    __tablename__ = 'candidate_organizations'

    candidate_org_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    
    cid = db.Column(db.String(100), db.ForeignKey('candidates.cid'), nullable=True)
    org_id = db.Column(db.String(100), db.ForeignKey('organizations.org_summary_id'), nullable=True)
    total = db.Column(db.Float(), nullable=False)
    pacs = db.Column(db.Float(), nullable=True)
    individuals = db.Column(db.Float(), nullable=True)

    orgs = db.relationship('Organization', foreign_keys=[org_id])

    candidate = db.relationship('Candidate', foreign_keys=[cid])

    # candidate = db.relationship('Candidate', backref=db.backref('candidate_organizations', order_by=candidate_org_id))

    # organization = db.relationship('Organization', backref=db.backref('candidate_organizations', order_by=candidate_org_id))











#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///candidata'
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