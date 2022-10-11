import covalent as ct
import requests
import json

districtapi = "https://api.covid19india.org/state_district_wise.json"
stateapi= "https://api.covid19india.org/data.json"

@ct.electron
def statewise_data(district,stateapi):
    stateresponse = requests.request("GET", stateapi)
    statedata =json.loads(stateresponse.text)
    return statedata

@ct.electron
def districtwise_data(districtapi):
    districtresponse = requests.request("GET", districtapi)
    districtdata =json.loads(districtresponse.text)
    return districtdata    



@ct.lattice
def gather_covid_data(districtapi,stateapi):
    district = districtwise_data(districtapi)
    return statewise_data(district,stateapi)
dispatcher=ct.dispatch(gather_covid_data)
both_id=dispatcher(districtapi,stateapi)