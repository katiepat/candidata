"""Utility file for gathering data on API"""


from sys import argv
import json
import requests
import time

from sqlalchemy import func
from server import app
from model import Candidate, Candidate_Summary, Candidate_Industry, Industry, Organization, Candidate_Organization, connect_to_db, db



# create variable to store api key
api_key = '7812644905e2e95248492bd13c40168a'

output = 'json'

payload = {}


url = 'https://opensecrets.org/api/'




def handle_ref():
    """ Turn txt doc into python dictionary """
  
   
    with open('data/cand_ids.txt') as txt:
        for line in txt:
            (CID, cand_name, party_id, district_id, fec_cand_id) = line.strip().split("\t")

            

        
            candidate = Candidate(cid=CID, cand_name=cand_name, 
                                party_id=party_id, district_id=district_id)
        
            db.session.add(candidate)

            db.session.commit()


            # cands.append(CID)
            

    return print('All Done')

def get_missing_org_names(cids):
    
    candidates = Candidate_Organization.query.filter(Candidate_Organization.org_name == None).all()
    print(candidates)    
 


def get_cand_summary(cids):
    """ takes in list of candidate ids, creates request and returns list of responses"""
    

    for cid in cids:

        payload = {'method': 'candSummary',
                'cid': cid,
                'apikey': api_key,
                'output': 'json',
                'cycle': '2018'
                }

        

       
        response = requests.get(url, params=payload)

        if response:

            candidate_summary = response.json()

            json.dump(candidate_summary, open('data/candidate_summary_backup.json', 'a'))

            candidate_summary = candidate_summary['response']['summary']['@attributes']


            cand_name = candidate_summary['cand_name']
            cid = candidate_summary['cid']
            state = candidate_summary['state']
            party = candidate_summary['party']
            chamber = candidate_summary['chamber']
            first_elected = candidate_summary['first_elected']
            total = float(candidate_summary['total'])
            spent = float(candidate_summary['spent'])
            cash_on_hand = float(candidate_summary['cash_on_hand'])

            debt = float(candidate_summary['debt'])


            summary = Candidate_Summary(cid=cid, state=state, chamber=chamber, 
                first_elected=first_elected, total=total, spent=spent, cash_on_hand=cash_on_hand,
                debt=debt)

            db.session.add(summary)

            db.session.commit()
        
      

    return print('All Done')    
       
           



def get_cand_industries(cids):
    """takes in list of candidate ids for request and returns list of response objects"""
    
    
    for cid in cids:

        payload = {'method' : 'candIndustry',   
                    'apikey': api_key,
                    'cid': cid,
                    'output': 'json',
                    'cycle': '2018'}
        
        response = requests.get(url, params=payload)

        if response:
            candidate_industries = response.json()

            # adds json to backup file
            json.dump(candidate_industries, open('data/top_industries.json', 'a'))

            
            #format json response
            candidate_industries = candidate_industries['response']['industries']
            
            

            # save candidate id
            cid = candidate_industries['@attributes']['cid']

           # gets the list of industries from the response
            industry_list = candidate_industries['industry']

            
            #loops through industry list
            for industry in industry_list:

                if type(industry) == dict:

                    industry_id = industry['@attributes']['industry_code']
                    industry_name = industry['@attributes']['industry_name']
                    indivs = float(industry['@attributes']['indivs'])
                    pacs = float(industry['@attributes']['pacs'])
                    total = float(industry['@attributes']['total'])

                    # checks industry table for industry id
                    if Industry.query.get(industry_id):


                        #if industry is in the table, only instantiate candidate_industry object
                        cand_industry = Candidate_Industry(cid=cid, industry_id=industry_id, 
                                        total=total, total_from_indivs=indivs, 
                                        total_from_pacs=pacs)

                        db.session.add(cand_industry)
                        db.session.commit()

                    else:

                        #if industry is not in table, instantiate both industry object and candidate_industry object
                        industry = Industry(industry_id=industry_id, industry_name=industry_name)

                        cand_industry = Candidate_Industry(cid=cid, industry_id=industry_id, 
                                        total=total, total_from_indivs=indivs, 
                                        total_from_pacs=pacs)
        
                        db.session.add(industry)
                    
                        db.session.add(cand_industry)
                        db.session.commit()

            # time.sleep(30)

    db.session.commit()
       



            
            
       
    return print('All Done')    



def get_org_id(org_name):
    """ function that makes API call to CRP to check for org_id"""

    payload = {'method' : 'getOrgs',
                'apikey': api_key,
                'org': org_name,
                'output': 'json'}
    
    response = requests.get(url, params=payload)



    if response:
        organizations = response.json()

        json.dump(organizations, open('data/get_org_id.json', 'a'))
        

        
        orgs = organizations['response']['organization']


        if type(orgs) is list:

            
            # org_ids = []

            for org in orgs:


                org_id = org['@attributes']['orgid']
                org_name = org['@attributes']['orgname']


                # checks to see if org is in db and if not calls get_org_summary function using id derived from API response
                if Organization.query.filter(Organization.org_name == org_name).all() == None:

                #    

                    org_summary = get_org_summary(org_id)

                   
                    print('All Done')

                    #returns true if org summary object instantiated
                    return True    
            
    else:
        #returns false if org summary object not instantiated
        return False    



             



    
def get_cand_contributions(cids):
    """ takes in list of candidate ids and returns list of response objects"""                           


    for cid in cids:
        payload = {'method' : 'candContrib',
                    'apikey': api_key,
                    'cid': cid,
                    'output': 'json',
                    'cycle': '2018'}

        response = requests.get(url, params=payload)

        if response:
        
            organizations = response.json()


            json.dump(organizations, open('data/top_contributors_backup.json', 'a'))

            if organizations == 'Resource not found':
                pass

            else:    

                organizations = organizations['response']['contributors']

                if organizations:

                    cid = organizations['@attributes']['cid']


                    organizations = organizations['contributor']

                    if type(organizations) != str:

                        for organization in organizations:
                            if type(organization) == dict:

                                org_name = organization['@attributes']['org_name']
                                total = float(organization['@attributes']['total'])
                                pacs = float(organization['@attributes']['pacs'])
                                indivs = float(organization['@attributes']['indivs']) 

                                #create candidate_org object using new 


                                cand_orgs = Candidate_Organization(cid=cid, org_name=org_name, total=total, pacs=pacs, individuals=indivs)
                                
                                db.session.add(cand_orgs)

                                db.session.commit()

                                #if org_id is true --> organization was instantiated in org_summary function
                                # org_id = get_org_id(org_name)

                                # #checks to see if org name is in the organization table
                                # org_query = Organization.query.filter(Organization.org_name == org_name).first()
                             
                                # #if org wasn't instantiated in the get_org_id function and if the database doesn't return an object, instantiate an org object
                                # if org_id == False and org_query == None:

                                    
                                    
                                #     organization = Organization(org_name=org_name, total=total, total_from_org_pac=pacs, total_from_indivs=indivs)

                                #     db.session.add(organization)
                                #     db.session.commit()


                                # #if org wasn't instantiated in the get_org_id but database is returning an org object with that name
                                # elif org_id == False and org_query != None:

                                #     #updates org totals, and commit to database

                                #     org_query.total += total

                                #     org_query.total_from_org_pac += pacs

                                #     org_query.total_from_indivs += indivs

                                #     db.session.add(org_query)
                                #     db.session.commit()

def update_state():

    candidates = Candidate.query.all()

    for candidate in candidates:
        district_id = candidate.district_id
        cid = candidate.cid

        state = district_id[:2]

        print(state)

        candidate_summary = Candidate_Summary.query.filter(Candidate_Summary.cid.like(f'%{cid}')).first()

        if candidate_summary:
            candidate_summary.state = state

            db.session.add(candidate_summary)
            db.session.commit()







def update_chamber():

    candidates = Candidate.query.all()


    for candidate in candidates:
        district_id = candidate.district_id
        # print(district_id)
        cid = candidate.cid

        senate = 'S1'
        state = district_id[:2]
        district_id = district_id[2:]
        # print(district_id)


        if district_id == senate:

            candidate_summary = Candidate_Summary.query.filter(Candidate_Summary.cid.like(f'%{cid}')).first()


            # print(candidate_summary)

            if candidate_summary:


                candidate_summary.chamber = 'S'

                db.session.add(candidate_summary)
                db.session.commit()

        
        else:
            candidate_summary = Candidate_Summary.query.filter(Candidate_Summary.cid.like(f'%{cid}')).first()
            
            if candidate_summary:
                candidate_summary.chamber = 'H'

                db.session.add(candidate_summary)
                db.session.commit()    




                               

def get_org_summary(org_id):


    payload = {'method': 'orgSummary',
                'apikey' : api_key,
                'id': org_id,
                'output': 'json'}

    response = requests.get(url, params=payload)


    if response:
        org_summary = response.json()

        json.dump(org_summary, open('data/organization_summary_backup.json', 'a'))

        org_summary = org_summary['response']['organization']['@attributes']

        crp_id = org_summary['orgid']
        org_name = org_summary['orgname']
        total = float(org_summary['total'])
        indivs = float(org_summary['indivs'])
        pacs = float(org_summary['pacs'])
        soft = float(org_summary['soft'])
        tot527 = float(org_summary['tot527'])
        dems = float(org_summary['dems'])
        repubs = float(org_summary['repubs'])
        lobbying = float(org_summary['lobbying'])
        outside = float(org_summary['outside'])
        mems_invested = int(org_summary['mems_invested'])
        gave_to_pac = float(org_summary['gave_to_pac'])
        gave_to_party = float(org_summary['gave_to_party'])
        gave_to_527 = float(org_summary['gave_to_527'])
        gave_to_cand = float(org_summary['gave_to_cand'])


        


        organization = Organization(org_name=org_name, total=total, crp_id=crp_id,
                        total_from_indivs=indivs, total_from_org_pac=pacs, total_soft_money=soft, 
                        total_from_527=tot527, total_to_dems=dems, total_to_repubs=repubs, 
                        total_spent_on_lobbying=lobbying, total_spent_on_outside_money=outside, num_members_invested=mems_invested, 
                        gave_to_pac=gave_to_pac, gave_to_party=gave_to_party, gave_to_527=gave_to_527, gave_to_cand=gave_to_cand)


        db.session.add(organization)
        db.session.commit()






def get_house_winners():

    candidates = db.session.query(Candidate.cand_name, Candidate.cid, Candidate.district_id).all()
    
    
 

    names_to_check = []


      
    
    with open('data/district_house_winners.txt') as txt:
        for line in txt:
        
            line = line.rstrip().split(" ")
            name = [line[0], line[1]]

            name_join = " ".join(name)


            candidate = Candidate.query.filter(Candidate.cand_name.like(f'%{name_join}%')).first()
            
            if candidate:
                candidate.win = True

                db.session.add(candidate)
                db.session.commit()

            else:
                names_to_check.append(name_join)
            


    return names_to_check
            # candidate = candidate_sets.get(name_join)

def add_summary_id():

    summaries_to_check = []


    candidates = Candidate.query.all()

    for candidate in candidates:
        cid = candidate.cid

        candidate_summary = Candidate_Summary.query.filter(Candidate_Summary.cid.like(f'%{cid}')).first()
        
        if candidate_summary:
            summary_id = candidate_summary.cand_summary_id
            candidate.cand_summary_id = summary_id
            db.session.add(candidate)
            db.session.commit()

        else:
            summaries_to_check.append(candidate)

    return summaries_to_check            



def get_contributor_names():


    file = open('data/top_contributors_backup.json').read()

    file = file.split()


    

    # file = file.split()

    # counter = 1

    for line in file:

        
        if item == 'cid':
            cid = line[item] + 1
            print(cid)



        

        # counter += 1

        # line = line.get('@attributes')

        # if line:

        # cid = line['cid']

        # candidate_contributors = Candidate_Organization.query.filter(Candidate_Organization.cid == cid).all()
        # print(candidate_contributors)

        # organizations = line['contributor']

        # if type(organizations) != str:

        #     for organization in organizations:
        #         if type(organization) == dict:

        #             org_name = organization['@attributes']['org_name']
        #             total = float(organization['@attributes']['total'])
        #             pacs = float(organization['@attributes']['pacs'])
        #             indivs = float(organization['@attributes']['indivs']) 

        #             # create candidate_org object using new

        #             for contributor in candidate_contributor:
        #                 if contributor.total == total and contributor.pacs == pacs and contributor.indivs == indivs:
        #                     contributor.org_name = org_name
        #                     db.session.add(contributor)
        #                     db.session.commit()

                        
                                 




def get_senate_winners():
    """ seeds list of winner"""

    names_to_check = []


    with open('data/senate_winners.txt') as txt:
        for line in txt:
            name = line.rstrip()

            candidate_query = Candidate.query.filter(Candidate.cand_name.like(f'%{name}%')).first()

            if candidate_query != None:
                
                candidate_query.win = True
                
                db.session.add(candidate_query)
                
                db.session.commit()

            else:
                names_to_check.append(name)

    return names_to_check
                                
        




def get_daily_list():

   

    candidate_ids = []


    with open('cand_ids.txt') as txt:
        for line in txt:
            (CID, cand_name, party_id, district_id, fec_cand_id) = line.strip().split("\t")

            candidate_ids.append(CID)


    return candidate_ids          


   
# def json_parsing():

#     #using backup file, add json as objects to db:
#     # query db for organizations that are not in organizations
#     #make the org_name the primary_key (because org_id is a string)
#     #maybe open file into a list

#     #add org_id and org_name to organization table


#     # contributor_list = []

#     with open('data/top_contributors_backup.json') as f:

#         dictionary = {}

#         for line in f:

#             # contributors = line.split('\n')
#             contributors = line.split()
#             print(contributors)

#             index = 0

#             for item in contributors:
#                 print((index, item))

#                 index+=1

#             cid = contributors[8]
#             contrib_list = contributors[46:]

#             dictionary[cid] = contrib_list

#         print(dictionary)


#         # for cid in dictionary.key:


            







               



        








if __name__ == "__main__":
    connect_to_db(app)
        





