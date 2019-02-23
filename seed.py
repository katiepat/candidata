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

LAST_UPDATED = {}

DAILY_LIMIT = 200


#display on html (move to server file)
CONTRIBUTORS_NOTICE = ""
# cands = {}

def handle_ref():
    """ Turn txt doc into python dictionary """
  
    # cids = []
    # parse txt file and tokenize rows
    with open('cand_ids.txt') as txt:
        for line in txt:
            (CID, cand_name, party_id, district_id, fec_cand_id) = line.strip().split("\t")

            

        
            candidate = Candidate(cid=CID, cand_name=cand_name, 
                                party_id=party_id, district_id=district_id)
        
            db.session.add(candidate)

            db.session.commit()


            # cands.append(CID)
            

    return print('All Done')

    
 


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
        
        # else:
        #     pass    


        time.sleep(30)

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

            json.dump(candidate_industries, open('data/top_industries.json', 'a'))

            if type(candidate_industries) == dict:

                candidate_industries = candidate_industries['response']['industries']

                cid = candidate_industries['@attributes']['cid']

               
                industry_list = candidate_industries['industry']

                if type(industry_list) == dict:

                    for industry in industry_list:

                        industry_id = industry['@attributes']['industry_code']
                        industry_name = industry['@attributes']['industry_name']
                        indivs = float(industry['@attributes']['indivs'])
                        pacs = float(industry['@attributes']['pacs'])
                        total = float(industry['@attributes']['total'])

                        if Industry.query.get(industry_id):


                            cand_industry = Candidate_Industry(cid=cid, industry_id=industry_id, 
                                            total=total, total_from_indivs=indivs, 
                                            total_from_pacs=pacs)

                        else:

                            industry = Industry(industry_id=industry_id, industry_name=industry_name)

                            cand_industry = Candidate_Industry(cid=cid, industry_id=industry_id, 
                                            total=total, total_from_indivs=indivs, 
                                            total_from_pacs=pacs)
            
                            db.session.add(industry)
                        
                        db.session.add(cand_industry)

                    time.sleep(30)

            db.session.commit()
           



            
            
       
        return print('All Done')    





def get_org_id(org_name):


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

            
            for org in orgs:


                org_id = org['@attributes']['orgid']
                org_name = org['@attributes']['orgname']

                # org_ids.append(org_id)

                if Organization.query.get(org_id) == None:

                    org_id = get_org_summary(org_id)

                    print('All Done')
                # return org_ids
        

        else:

            org_id = orgs['@attributes']['orgid']
            org_name = orgs['@attributes']['orgname']

            if Organization.query.get(org_id) == None:

                org_summary = get_org_summary(org_id)

                print('All Done')
            # print('All Done')

            # return org_ids       



    
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

                    # orgs = organizations['contributor']

                    organizations = organizations['contributor']

                    if type(organizations) != str:

                        for organization in organizations:
                            if type(organization) == dict:

                                org_name = organization['@attributes']['org_name']
                                total = float(organization['@attributes']['total'])
                                pacs = float(organization['@attributes']['pacs'])
                                indivs = float(organization['@attributes']['indivs'])


                                # org_id = get_org_id(org_name)  

                                cand_orgs = Candidate_Organization(cid=cid, total=total, pacs=pacs, individuals=indivs)
                                
                                db.session.add(cand_orgs)
                                

                                
                                org = get_org_id(org_name)

                               
                                db.session.commit()
                
                                time.sleep(30)

        #pause for one min for each request

    
 
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

        org_id = org_summary['orgid']
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


        


        organization = Organization(org_summary_id=org_id, org_name=org_name, total=total,
                        total_from_indivs=indivs, total_from_org_pac=pacs, total_soft_money=soft, 
                        total_from_527=tot527, total_to_dems=dems, total_to_repubs=repubs, 
                        total_spent_on_lobbying=lobbying, total_spent_on_outside_money=outside, num_members_invested=mems_invested, 
                        gave_to_pac=gave_to_pac, gave_to_party=gave_to_party, gave_to_527=gave_to_527, gave_to_cand=gave_to_cand)


        db.session.add(organization)
        db.session.commit()


        



def get_daily_list():

    #figure out how to request a certain number of items every day

    # ref = handle_ref()

    candidate_ids = []

    candidates_to_do = []

    with open('cand_ids.txt') as txt:
        for line in txt:
            (CID, cand_name, party_id, district_id, fec_cand_id) = line.strip().split("\t")

            candidate_ids.append(CID)


    return candidate_ids          


   

   







if __name__ == "__main__":
    connect_to_db(app)
        





