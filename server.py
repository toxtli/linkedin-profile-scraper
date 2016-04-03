import json
from LinkedinController import LinkedinController

linkedinTool = LinkedinController()
url = 'https://www.linkedin.com/in/toxtli'
profile = linkedinTool.extractProfile(url)
print json.dumps(profile)