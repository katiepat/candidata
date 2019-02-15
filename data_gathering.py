"""Utility file for gathering data on API"""


from sys import argv
import json
import requests
import time

# create variable to store api key
api_key = '7812644905e2e95248492bd13c40168a'

output = 'json'

payload = {}

completed = []

url = 'https://opensecrets.org/api/'


#create variable for url and params
# response = requests.get(url, params=payload)

cands = {}

def handle_ref():
    """ Turn txt doc into python dictionary """
  

    # parse txt file and tokenize rows
    with open('cand_ids.txt') as txt:
        for line in txt:
            (CID, cand_name, party, dist_id, fec_cand_id) = line.strip().split("\t")

            cands[CID] = [cand_name, party, dist_id]

    return cands

def get_cid_list():
    """ Gets list of all CIDs in dictionary and returns list of candidate ids"""
    cids = []

    for key in cands.keys():
        CID = key
        cids.append(CID)

    return cids


def get_cand_summary(cids):
    """ takes in list of candidate ids, creates request and returns list of responses"""
    

    cand_summaries = []

    for cid in cids:

        payload = {'method': 'candSummary',
                'cid': cid,
                'apikey': api_key,
                'output': 'json'
                }

        

        #may not need to convert to json
        response = requests.get(url, params=payload)

        #instantiate class object and commit to db
                

        # cand_summaries.append(response)

        time.sleep(60)
       

    return cand_summaries            



def get_cand_industries(cids):
    """takes in list of candidate ids for request and returns list of response objects"""
    
    cand_industries = []

    for cid in cids:
        payload = {'method' : 'candIndustry',   
                    'apikey': api_key,
                    'cid': cid,
                    'output': 'json'}
        
        response = requests.get(url, params=payload)


        #instantiate class object and commit to db

        # cand_industries.append(response)
        
        time.sleep(60)

    return cand_industries
    
def get_cand_contributions(cids):
    """ takes in list of candidate ids and returns list of response objects"""                           

    cand_contribs = []


    for cid in cids:
        payload = {'method' : 'candContrib',
                    'apikey': api_key,
                    'cid': cid,
                    'output': 'json'}

        response = requests.get(url, params=payload)
        
        #instantiate class object and commit to db


        
        # cand_contribs.append(response)

        time.sleep(60)

        #pause for one min for each request

    return cand_contribs
 
def get_daily_list():

    ref = handle_ref()

    cids = get_cid_list() #splice to two hundred

    daily_limit = cids[:200]


    return daily_limit

def request_looping():
    """runs loop for data requests """
    

    #gets list of 200 candidate ids
    cids = get_daily_list()
    
    #gets candidates summary using result of get_daily_list()
    get_cand_summary(cids)

    time.sleep(30)

    
    # completed = completed.append(cids)
    
    #get top candidate industries using result of get_daily_list()
    get_cand_industries(cids)

    time.sleep(30)

    #get top contributors using result of get_daily_list()
    get_cand_contributions(cids)



    # #return list of completed ids???
    # completed = completed.append(cids)

    # return completed

        





