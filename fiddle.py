
import requests

import logging
from http.client import HTTPConnection

# Enable HTTPConnection debug logging to console
HTTPConnection.debuglevel = 1

# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

url = "https://karholl.is"
url ="https://karholl.is/images/news/2023/Halldor_shows_He_Rulong_The_Ground_Floor.jpg"


url
r = requests.get(url)
r.status_code
