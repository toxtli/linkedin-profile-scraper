# python batch.py -c ../../config/linkedin-old -l ../../data/list-tech.json -n 10 -f 0 -t 1

import sys
import time
import getopt
import random
import simplejson
from pymongo import MongoClient
from LinkedinController import LinkedinController

DB_NAME = 'test'
DB_COL = 'lnprofilestech'

def main(params):
    config_file = None
    list_file = None
    num_messages = 99999
    wait_time_from = 0
    wait_time_to = 0
    opts, args = getopt.getopt(params, "l:n:c:f:t:")
    if opts:
        for o, a in opts:
            if o == "-c":
                config_file = a
            elif o == "-l":
                list_file = a
            elif o == "-f":
                wait_time_from = int(a)
            elif o == "-t":
                wait_time_to = int(a)
            elif o == "-n":
                num_messages = int(a)
    linkedin_tool = LinkedinController(config=config_file, debug=True)
    urls = []
    if list_file:
        urls = simplejson.loads(open(list_file).read())
    else:
        urls = ['https://www.linkedin.com/in/toxtli']

    client = MongoClient()
    db = client[DB_NAME]
    col = db[DB_COL]
    counter = 0
    for url in urls:
        if not col.find_one({'_id': url}):
            if counter < num_messages:
                counter += 1
                print counter
                print 'PROCESSING ...'
                print url
                profile = linkedin_tool.extractProfile(url)
                profile['_id'] = url
                col.insert_one(profile)
                print 'DONE'
                wait_time = random.randint(wait_time_from, wait_time_to)
                time.sleep(wait_time)
            else:
                break
        else:
            print 'NEXT'

if __name__ == "__main__":
    argv = sys.argv[1:]
    main(argv)