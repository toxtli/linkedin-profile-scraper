# Extracting public profile:
# python profile.py -u http://www.linkedin.com/in/toxtli
#
# Extracting user from a logged in account:
# python profile.py -u http://www.linkedin.com/in/toxtli -c linkedin-config

import sys
import json
import getopt
from LinkedinController import LinkedinController

def main(params):
	config_file = None
	url = None
	opts, args = getopt.getopt(params, "u:c:")
	if opts:
		for o, a in opts:
			if o == "-c":
				config_file = a
			elif o == "-u":
				url = a
	linkedinTool = LinkedinController(config=config_file, debug=True)
	profile = linkedinTool.extractProfile(url)
	print json.dumps(profile)

if __name__ == "__main__":
    argv = sys.argv[1:]
    main(argv)