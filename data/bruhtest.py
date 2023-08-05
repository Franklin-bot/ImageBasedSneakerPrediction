import requests
from requests_ip_rotator import ApiGateway
from bs4 import BeautifulSoup

url = "https://stockx.com/balenciaga-triple-s-indigo"



# # Create gateway object and initialise in AWS
gateway = ApiGateway(url)
gateway.start()

# Assign gateway to session
session = requests.Session()
session.mount(url, gateway)

# Send request (IP will be randomised)
response = session.get(url + "/index.php", params={"theme": "light"})
soup = BeautifulSoup(response.text, 'html')
print(soup)

# Delete gateways
gateway.shutdown()