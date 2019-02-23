"""Campaign finance tracker"""

from jinja2 import StrictUndefined


from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import Candidate, Candidate_Summary, Candidate_Industry, Industry, Organization, Candidate_Organization, connect_to_db, db


app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined



STATES = {'AL': 'Alabama', 'AK':'Alaska', 'AZ':'Arizona', 'AR':'Arkansas', 
        'CA': 'California', 'CO':'Colorado', 'CT':'Connecticut', 'DE': 'Delaware',
        'FL': 'Florida', 'GA': 'Georgia', 'HI':'Hawaii', 'ID':'Idaho', 'IL': 'Illinois',
        'IN': 'Indiana', 'IA':'Iowa', 'KS':'Kansas', 'KY': 'Kentucky', 'LA':'Louisiana',
        'ME': 'Maine', 'MD': 'Maryland', 'MA':'Massachusetts', 'MI': 'Michigan', 
        'MN':'Minnesota', 'MS':'Mississippi', 'MO': 'Missouri', 'MT': 'Montana',
        'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
        'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota',
        'OH': 'Ohio', 'OK': 'Oklahoma', 'OR':'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island',
        'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas',
        'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
        'WI': 'Wisconsin', 'WY': 'Wyoming'}

#########################################################################################################



@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/districts', methods=['GET'])
def get_districts():
    """Shows form to get districts by state"""

    


    return render_template("districts.html", states=STATES, candidates=candidates)




@app.route('/candidates', methods=['GET'])
def candidates_list():
    """Show list of Candidates"""

    candidates = Candidate_Summary.query.all()



    return render_template("candidates.html", states=STATES, candidates=candidates)



@app.route('/candidates', methods=['GET'])
def get_candidate_form():

    state = request.args.get('state')

    chamber = request.args.get('chamber')

    candidates = Candidate_Summary.query.filter(Candidate_Summary.state==state, Candidate_Summary.chamber==chamber).all()

    return render_template('candidates.html', candidates=candidates)





@app.route('/candidates/<cid>', methods=['GET'])
def candidate_cycle_summary(cid):   
    """ Get summary information for candidate, based on input id """

    #write query for cid in db--> return summary information
    candidate = Candidate.query.get(cid)

    candidate_summary = Candidate_Summary.query.filter(Candidate_Summary.cid == cid).all()

    contributors = Candidate_Organization.query.filter(Candidate_Organization.cid == cid).all()

    industries = Candidate_Industry.query.filter(Candidate_Industry.cid == cid).all()

    return render_template("candidate.html", 
                        candidate=candidate,
                        candidate_summary=candidate_summary, 
                        contributors=contributors, 
                        industries=industries)







@app.route('/organizations')
def organization_list():
    """show list of organizations who were top contributors to 2018 cycle"""

    organization_list = Organization.query.all()

    return render_template("organizations.html", organizations=organization_list)






@app.route('/organizations/<org_summary_id>', methods=['GET'])
def get_organization_summary(org_summary_id):
    """display organization summary"""



    organization = Organization.query.get(org_summary_id)

    return render_template('organization.html', organization=organization)


# @app.route('/districts', methods=['GET'])
# def get_district_form():
#     """ shows list of districts by state"""

#     state = request.args.get('state')
#     chamber = request.args.get('chamber')

#     candidates = Candidate_Summary.query.filter(Candidate_Summary.state == state, Candidate_Summary.chamber == chamber).all()



#     return render_template('districts_by_state.html', candidates=candidates)



# @app.route('/districts/<int:district_id>', methods=['GET'])
# def district_race(district_id):
#     """Show information for selected district"""

    

#     state = request.args.get('state')
#     chamber = request.args.get('chamber')

#     candidates = Candidate.query.filter(Candidate.Candidate_Summary.state == state, Candidate.Candidate_Summary.chamber == chamber).all()

    

#     return render_template("district.html", district=district_id, candidates=candidates) 






if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")    