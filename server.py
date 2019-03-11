"""Campaign finance tracker"""

from jinja2 import StrictUndefined


from flask import Flask, render_template, request, flash, redirect, session, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension

from model import Candidate, Candidate_Summary, Candidate_Industry, Industry, Organization, Candidate_Organization, connect_to_db, db


app = Flask(__name__)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False

app.secret_key = 'ABC'

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

    candidate_totals = Candidate_Summary.query.all()

    sum_total = 0

    for candidate in candidate_totals:
        total = candidate.total

        sum_total += total

    # total_cycle = sum(float(total_cycle))


    num_candidates = Candidate.query.count()

    top_25_house_cands = Candidate_Summary.query.filter(Candidate_Summary.chamber =="H").order_by(Candidate_Summary.total.desc()).limit(25)
    
    top_10_senators = Candidate_Summary.query.filter(Candidate_Summary.chamber =="S").order_by(Candidate_Summary.total.desc()).limit(10)
    sum_total = "{:,}".format(int(sum_total))

    return render_template('homepage.html', sum_total=sum_total, num_candidates=num_candidates, top_25_house_cands=top_25_house_cands, top_10_senators=top_10_senators)





@app.route('/json')
def show_summary_data():

    reps = Candidate.query.filter(Candidate.party_id == 'D').all()
    dems = Candidate.query.filter(Candidate.party_id == 'R').all()

    others = Candidate.query.filter(Candidate.party_id != 'D', Candidate.party_id != 'R').all()

    reps_total = 0

    dems_total = 0

    others_total = 0

    for rep in reps:
        cid = rep.cid

        cand_summary = Candidate_Summary.query.filter(Candidate_Summary.cid == cid).first()

        if cand_summary:

            total = float(cand_summary.total)

            reps_total += total

    for dem in dems:
    
        cid = dem.cid

        cand_summary = Candidate_Summary.query.filter(Candidate_Summary.cid == cid).first()

        if cand_summary:

            total = float(cand_summary.total)

            dems_total += total  

    for other in others:
        cid = other.cid
        cand_summary = Candidate_Summary.query.filter(Candidate_Summary.cid == cid).first()


        if cand_summary:
            total = float(cand_summary.total)
            others_total += total


    # reps_total = "{:,}".format(reps_total)
    # dems_total = "{:,}".format(dems_total)
    # others_total = "{:,}".format(others_total)
    

    data_dict = {
                'datasets' : [
                {
                    'data' : [reps_total, dems_total, others_total],
                    'backgroundColor' : ['#FF0000', '#4EC7EC', '#A9A9A9']
                }],
                'labels' : ['Republican Party', 'Democratic Party', 'Other Party']
                
}

    return jsonify(data_dict)    

# @app.route('/winners_losers.json')
# def show_winner_loser_chart():

#     candidates = Candidate_Summary.query.all()



    





@app.route('/district_summaries.json')
def show_district_summary_graph():
    
    

    cand_by_district = Candidate.query.all()
    
    # print(races_by_district)
    bad_ids = {'NVS1', 'UTS1', 'VTS1', 'FLS1', 'MNS1', 'MTS1', 'MAS1', 'RIS1', 'MIS2', 'NDS2', 'NMS1', 'HIS2', 'MSS2', 'WYS1', 'PAS2', 'NJS1'}
    district_ids = []

    reps_total = []
    dems_total = []
    third_total = []

    for cand in cand_by_district:
        if cand.district_id[2:] == "S1" or cand.district_id[2:] == "S2":
            if cand.district_id not in district_ids:
            
                district_id = cand.district_id
                # district_ids.append(district_id)
                cand_sum = Candidate_Summary.query.filter(Candidate_Summary.cid == f'{cand.cid}').first()
                if cand_sum:
                    if cand.party_id == "R":
                        # cand_sum = Candidate_Summary.query.filter(Candidate_Summary.cid == f'{cand.cid}').first()
                        # if cand_sum:
                        total = float(cand_sum.total)
                        if total > 0:  
                            reps_total.append(total)
                            # district_ids.append(district_id)

                    elif cand.party_id == "D":
                        # cand_sum = Candidate_Summary.query.filter(Candidate_Summary.cid == f'{cand.cid}').first()
                        
                        # if cand_sum:
                        total = float(cand_sum.total)

                        if total > 0:   
                            dems_total.append(total)
                            # district_ids.append(district_id)
                    else:
                        # cand_sum = Candidate_Summary.query.filter(Candidate_Summary.cid == f'{cand.cid}').first()
                            
                        

                        total = float(cand_sum.total)
                        if total > 0:
                        

                            third_total.append(total)
                            # district_ids.append(district_id)
                    

                    if district_id not in bad_ids:        
                        district_ids.append(district_id)
            else:
                    pass             


    data_dict = {

        'labels' : district_ids,
        
        'datasets' : [
            {
            'label' : 'Republican Party Candidate',
            'backgroundColor': '#FF0000',
                'data' : reps_total
            }, {
            'label' : 'Democratic Party Candidate',
            'backgroundColor' : '#4EC7EC',
            'data': dems_total
            }, {
            'label' : 'Third Party Candidate',
            'backgroundColor': '#A9A9A9',
            'data' : third_total
            }] }


    return jsonify(data_dict)        





# @app.route('/candidates', methods=['GET'])
# def candidates_list():
#     """Show list of Candidates"""

#     # candidates = Candidate_Summary.query.order_by(Candidate_Summary.total.desc()).all()


#     # candidate_search = get("tags")
#     # print(candidate_search)
    
   


#     # candidates = Candidate.query.filter(Candidate.cand_name.like(f'% {candidate_search} %')).all()

#     top_25_house_cands = Candidate_Summary.query.filter(Candidate_Summary.chamber =="H").order_by(Candidate_Summary.total.desc()).limit(25)
    
#     top_10_senators = Candidate_Summary.query.filter(Candidate_Summary.chamber =="S").order_by(Candidate_Summary.total.desc()).limit(10)

#     # if len(candidates) == 1:

#     #     cid = candidates.cid
        

#     #     return redirect('/candidates/<cid>', cid=cid)

    

#     return render_template('candidates.html', states=STATES, top_10_senators=top_10_senators, top_25_house_cands=top_25_house_cands)

@app.route('/candidates', methods=['POST'])
def get_candidate_page():

    candidate_name = request.form.get('tags')
    print(candidate_name)
    print(type(candidate_name))

    candidate_lname, candidate_fname = candidate_name.rstrip().split()

    # candidate_fname = candidate_fname[:-1] 
    # candidate_lname = candidate_name[0]
    candidate_lname = candidate_lname[:-1]
    print(candidate_lname)
    # print(candidate_name)
    # print(candidate_name['value'])

    candidates = Candidate.query.all()
    # candidate_id = Candidate.query.filter(Candidate.cand_name.like('%cand_lname%')).first()
    # print(candidate_id.cid)
    # cid = candidate_id.cid
    for candidate in candidates:
        cand_name = candidate.cand_name
        cand_name = cand_name.rstrip().split()
        cand_fname = cand_name[1:-2]
        print(cand_fname)
        
        cand_lname = cand_name[0]
        cand_lname = cand_lname[1:-1]


        print(str(cand_lname))
        print(str(candidate_lname))
        # print(type(cand_lname))    
        if str(cand_lname) == str(candidate_lname):
            print(candidate)
            # print(type(candidate))
            cid = candidate.cid
            print(cid)

    # print(cid)
    
            return redirect(f'candidates/{cid}')

@app.route('/what-does-it-all-mean')
def show_terms():

    return render_template('terms.html')




@app.route('/candidates/<cid>', methods=['GET'])
def candidate_cycle_summary(cid):   
    """ Get summary information for candidate, based on input id """

    #write query for cid in db--> return summary information
    candidate = Candidate.query.get(cid)

    winner = candidate.win

            


    candidate_name = candidate.cand_name


    candidate_name = candidate_name[1:(len(candidate_name)-1)]
 

    candidate_name = candidate_name.split(',')

    candidate_fname = candidate_name[1]
    candidate_lname = candidate_name[0]

    candidate_name = f'{candidate_fname} {candidate_lname}'

    candidate_summary = Candidate_Summary.query.filter(Candidate_Summary.cid == cid).first()


    opponents = Candidate.query.filter(Candidate.district_id == candidate.district_id, Candidate.cid != cid).all()
    
    if winner:
        winner = "Won"

    else:
        for opp in opponents:
            if opp.win:
                opp_name = opp.cand_name[1:(len(opp.cand_name)-1)]
                opp_name = opp_name.split(',')
                opp_fname = opp_name[1]
                opp_lname = opp_name[0]
                opp_name = f'{opp_fname} {opp_lname}'
                winner = f"Lost to {opp_name}"
            

 

    organizations = Candidate_Organization.query.filter(Candidate_Organization.cid == cid).all()


    industries = Candidate_Industry.query.filter(Candidate_Industry.cid == cid).all()

    total_by_top_contributors = 0
    percentage_from_top_contribs = float((total_by_top_contributors / candidate_summary.total)*100)

    for org in organizations:
        total = org.total
        total_by_top_contributors += total

    percentage_from_top_contribs = float((total_by_top_contributors / candidate_summary.total)*100)


    return render_template('candidate.html',
                    STATES=STATES,
                    winner=winner,
                    cid=cid, 
                    candidate=candidate,
                    candidate_name=candidate_name,
                    opponent=opponents,
                    candidate_summary=candidate_summary, 
                    organizations=organizations, 
                    total_by_top_contributors=total_by_top_contributors,
                    percentage_from_top_contribs=percentage_from_top_contribs)
        





@app.route('/candidates/<cid>/opponents.json')
def show_opponent_graph(cid):
    

    candidate = Candidate_Summary.query.filter(Candidate_Summary.cid == cid).first()
    total = candidate.total

    cand = Candidate.query.filter(Candidate.cid == cid).first()
    cand_name = cand.cand_name

    opponents = Candidate.query.filter(Candidate.district_id == cand.district_id, Candidate.cid != cid).all()
    
    data_list = [candidate.total]
    label_list = [cand_name]
    backgroundColor = []


    for opponent in opponents:

        cid = opponent.cid

        opp_name = opponent.cand_name

        party_id = opponent.party_id




        opp_summary = Candidate_Summary.query.filter(Candidate_Summary.cid == cid).first()
        
        if opp_summary:
            
            opp_total = opp_summary.total
            print(opp_total)

            label_list.append(opp_name)

            data_list.append(opp_total)

            if party_id == 'R':

                backgroundColor.append('#FF0000')
            elif party_id == 'D':
                backgroundColor.append('#4EC7EC')
            else:
                backgroundColor.append('#A9A9A9')        





    data_dict = {
                'datasets' : [
                {
                    'data' : [],
                    'backgroundColor' : backgroundColor
                }],
                'labels' : []
    }
    
    data_dict['labels'] = label_list
    data_dict['datasets'][0]['data'] = data_list

    if data_dict != None:    


        return jsonify(data_dict)





@app.route('/candidates/<cid>/industries.json')
def candidate_industry_data(cid):
    
    # candidate_orgs = Candidate_Organization.query.filter(Candidate_Organization.cid == cid).all()
    candidate_industries = Candidate_Industry.query.filter(Candidate_Industry.cid == cid).all()
    
    

    labels_list = []
    data_list = []

    for industry in candidate_industries:
        # name = industry.industry_id

        ind_name = Industry.query.get(industry.industry_id)
        
        
        labels_list.append(ind_name.industry_name)        
                

        total = industry.total

        data_list.append(total)


    data_dict = {
                'datasets' : [
                {
                    'data' : []
                }],
                'labels' : []
    }



    data_dict['labels'] = labels_list
    data_dict['datasets'][0]['data'] = data_list    


    return jsonify(data_dict)





@app.route('/candidates/<cid>/organizations.json')
def candidate_orgs_data(cid):

    candidate_orgs = Candidate_Organization.query.filter(Candidate_Organization.cid == cid).all()

    labels_list = []
    data_list = []

    for org in candidate_orgs:
        label = org.org_name
        data = float(org.total)
        print(data)

        labels_list.append(label)
        data_list.append(data)




    data_dict = {
                'datasets' : [
                {
                    'data' : []
                }],
                'labels' : []
    }
    data_dict['datasets'][0]['data'] = data_list
    data_dict['labels'] = labels_list

    return jsonify(data_dict)


@app.route('/organizations')
def organization_list():
    """show list of organizations who were top contributors to 2018 cycle"""

    organization_list = Organization.query.all()

    return render_template('organizations.html', organizations=organization_list)

@app.route('/organizations', methods=['POST'])
def organization_search():

    organization_list = Organization.query.all()

    org_name = request.form.get('tags')

    for org in organization_list:
        if org.org_name == org_name:

            org_id = org.org_id

            return redirect(f'organizations/{org_id}')



    



@app.route('/organizations/<org_id>', methods=['GET'])
def get_organization_summary(org_id):
    """display organization summary"""



    organization = Organization.query.get(org_id)

    org_name = organization.org_name

    print(org_name)

    candidates = []

    
    candidate_orgs = Candidate_Organization.query.filter(Candidate_Organization.org_name.like('%org_name%')).all()

    print(candidate_orgs)
    for org in candidate_orgs:
        cid = org.cid

        candidate = Candidate.query.get(cid)

        candidates.append(candidate)



    
    


    return render_template('organization.html', organization=organization, candidates=candidates, org_id=org_id)



@app.route('/organizations/<org_id>/raised.json')
def show_org_data(org_id):

    organization = Organization.query.get(org_id)



    if organization:
        total_from_individuals = int(organization.total_from_indivs)
        from_org_pac = int(organization.total_from_org_pac)
        from_527 = int(organization.total_from_527)
        soft_money = int(organization.total_soft_money)

        

        backgroundColor = ['#FF0000', '#4EC7EC', '#A9A9A9', 'fffdd0']
        labels_list = ["From Individuals", "From Organization's PAC", "From Organization's 527"]
        data_list= [total_from_individuals, from_org_pac, from_527, soft_money]




    data_dict = {
                'datasets' : [
                {
                    'data' : data_list,
                    'backgroundColor' : backgroundColor
                }],
                'labels' : labels_list
    }
    

    return jsonify(data_dict)


@app.route('/organizations/<org_id>/party-comparison.json')
def show_given_to_parties(org_id):

    organization = Organization.query.get(org_id)

    gave_to_reps = organization.total_to_repubs
    gave_to_dems = organization.total_to_dems

    backgroundColor = ['#FF0000', '#4EC7EC']
    data_list = [gave_to_reps, gave_to_dems]
    labels_list = ['Republican Party', 'Democratic Party']


    data_dict = {
                'datasets' : [
                {
                    'data' : data_list,
                    'backgroundColor' : backgroundColor
                }],
                'labels' : labels_list
    }
    

    return jsonify(data_dict)






if __name__ == '__main__':
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    

    app.run(host='0.0.0.0')    