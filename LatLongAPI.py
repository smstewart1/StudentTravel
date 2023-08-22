#libraries
import requests
from requests.structures import CaseInsensitiveDict



#main code
def main():
    
    #setup of the API
    url = "https://api.geoapify.com/v1/geocode/search?text=38%20Upper%20Montagu%20Street%2C%20Westminster%20W1H%201LJ%2C%20United%20Kingdom&apiKey=f48147c372e84fcdaf5c38ece413bffd"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    resp = requests.get(url, headers=headers)
    print(resp.status_code)
    
    #import the addressed to be used
    
    
    
    
    return


#functions



main()