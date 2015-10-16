import datetime

__author__ = 'jeff'
# TODO: figure out pydocs

import lib.Util as vtUtil
import lib.Domain as vtDomain
import json
import urllib
import pprint
import ConfigParser
from peewee import *

configurations = ConfigParser.RawConfigParser()
configurations.read('config.cfg')
API_KEY = configurations.get('virusTotal', 'public_key')
MAX_RECORD_AGE = configurations.getint('db', 'rescan_age_in_minutes')

Domain = vtDomain.Domain
db = SqliteDatabase('vtTool.db')

pp = pprint.PrettyPrinter(indent=4)

# connect
try:
    vtUtil.setup(db)
except OperationalError as e:
    if "already exists" in e.message:
        existing_db = e.message.split('"')[1::2][0]
        print "'{0}' db already exists.".format(existing_db)
    else:
        raise

# ingest file into db
with open('sampleDomains.txt', 'r') as f:
    for line in f:
        d = Domain.find_or_create_by_name(line.strip())
        print

# TODO: logger

# scan domains in db
for domain in Domain.select().order_by(Domain.created_on.desc()):
    print "Checking " + domain.name
    # if its older than a week... todo: put this in config.cfg file
    if domain.last_scanned is None or domain.last_scanned < datetime.datetime.now() - datetime.timedelta(
            minutes=MAX_RECORD_AGE):
        url = 'https://www.virustotal.com/vtapi/v2/domain/report'
        parameters = {'domain': domain.name, 'apikey': API_KEY}
        response = urllib.urlopen('%s?%s' % (url, urllib.urlencode(parameters))).read()
        response_dict = json.loads(response)
        # pp.pprint(response_dict)
        domain.vt_safety_score = response_dict['Webutation domain info']['Safety score']
        # print response_dict['detected_downloaded_samples'][0]['positives']
        domain.vt_number_of_ips = len(response_dict['resolutions'])
        domain.last_scanned = datetime.datetime.now()
        domain.status = 'scanned'
        domain.save()
    else:
        print "Domain was checked less than %s minutes ago." % MAX_RECORD_AGE



# for debug... list all domains in DB:
#
for domain in Domain.select().order_by(Domain.created_on.desc()):
    print domain.to_string()

db.close()

#todo: turn ingest and scan into functions; make workers; accept streaming
