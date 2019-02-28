"""Campaign finance tracker"""

from jinja2 import StrictUndefined


from flask import Flask, render_template, request, flash, redirect, session, jsonify
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

# @app.route('/districts', methods=['GET'])
# def get_districts():
#     """Shows form to get districts by state"""

    


#     return render_template("districts.html", states=STATES)




@app.route('/candidates', methods=['GET'])
def candidates_list():
    """Show list of Candidates"""

    candidates = Candidate_Summary.query.all()






    return render_template("candidates.html", states=STATES, candidates=candidates)



# @app.route('/candidates', methods=['GET'])
# def get_candidate_form():

#     state = request.args.get('state')

#     chamber = request.args.get('chamber')

#     candidates = Candidate_Summary.query.filter(Candidate_Summary.state==state, Candidate_Summary.chamber==chamber).all()

#     return render_template('candidates.html', candidates=candidates)





@app.route('/candidates/<cid>', methods=['GET'])
def candidate_cycle_summary(cid):   
    """ Get summary information for candidate, based on input id """

    #write query for cid in db--> return summary information
    candidate = Candidate.query.get(cid)

    candidate_name = candidate.cand_name

    candidate_name = candidate_name[1:(len(candidate_name)-1)]
 

    candidate_name = candidate_name.split(',')

    candidate_fname = candidate_name[1]
    candidate_lname = candidate_name[0]

    candidate_name = f"{candidate_fname}{candidate_lname}"

    candidate_summary = Candidate_Summary.query.filter(Candidate_Summary.cid == cid).first()

    opponent = Candidate.query.filter(Candidate.district_id == candidate.district_id, Candidate.cid != cid).all()
    
    # cand_orgs = Candidate_Organization.query.filter(Candidate_Organization.cid == cid).all()
    organizations = Candidate_Organization.query.filter(Candidate_Organization.cid == cid).all()

    # org_names = Organization.query.filter(Organization.org_summary_id == organizations.org_id).all()

    # organizations = Organization.query.filter(Organization.cand_orgs.cid == cid).all()

    # organizations = Candidate.query
    # org_info = []

    # for organization in organizations:
    #     name = Organization.query.filter(Organization.org_summary_id == organization.org_id).all()

    #     info = org_info.append(name)

    industries = Candidate_Industry.query.filter(Candidate_Industry.cid == cid).all()

    


    return render_template("candidate.html", 
                    candidate=candidate,
                    candidate_name=candidate_name,
                    opponent=opponent,
                    candidate_summary=candidate_summary, 
                    organizations=organizations, 
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

    # candidates = Candidate_Organization.query.filter(Candidate_Organization.org_id == org_summary_id).all()

    candidates = Candidate_Organization.query.filter(Candidate_Organization.org_id == org_summary_id).all()

    
    print(candidates)

    # cand_orgs = Candidate_Organization.query.filter_by(org_id = organization.org_summary_id).all()
    # print(cand_orgs)
    # cids = cand_orgs.cid.all()

    # cids = []
    # print(cids)

    # candidates = []

    # for org in cand_orgs:
        
    #     cid = org.cid
        
    #     cids.append(cid)


    # for cid in cids:
    #     candidate = Candidate.query.get(cid)

    #     candidates.append(candidate)    



    return render_template('organization.html', organization=organization, candidates=candidates, error_message=None)



@app.route('/districts', methods=['GET'])
def show_district_form():


    districts = Candidate.district_id.query.all()
#     districts = Candidate.query(Candidate.all()



    return render_template('districts_by_state.html', states=STATES)




# @app.route('/districts', methods=['GET'])
# def get_district_form():
#     """ shows list of districts by state"""

#     state = request.args.get('state')

#     # chamber = request.args.get('chamber')

#     # candidates = Candidate_Summary.query.filter(Candidate_Summary.state == state, Candidate_Summary.chamber == chamber).all()
#     districts = Candidate.query.filter(Candidate.district_id.like('%state%')).all()

    








    # return render_template('districts/district_by_state.html', districts=districts, state=state)



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