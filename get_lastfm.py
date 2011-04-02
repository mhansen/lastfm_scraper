#!/usr/bin/env python
from datetime import datetime 
import codecs
import gflags
import json
import sys
import time
import urllib
import urllib2

# Flag parsing, using google's awesome flag library
FLAGS = gflags.FLAGS
gflags.DEFINE_string("user", "Mark_Hansen", "Last.FM username")
try:
    argv = FLAGS(sys.argv)
except gflags.FlagsError, e:
    print "%s\nUsage: %s\n%s" % (e, sys.argv[0], FLAGS)
    sys.exit(1)


params = { "method":"user.getrecenttracks",
           "user": FLAGS.user,
           "api_key": "b25b959554ed76058ac220b7b2e0a026",
           "format": "json",
           "limit": "200" }
# Last.FM splits your scrobbles into pages of at most 200 scrobbles, so you
# need to loop through each page and download each one until you get them all.
def fetch_scrobble_page(num):
    "Fetches a page of recent scrobbles, with a page number"
    print "fetching page %s" % (num)
    params["page"] = num
    url = "http://ws.audioscrobbler.com/2.0/?" + urllib.urlencode(params)
    response = urllib2.urlopen(url)
    the_page = response.read()
    return json.loads(the_page)

scrobbles = []
def append_all_scrobbles_in_page(page):
    for scrobble in page['recenttracks']['track']:
        scrobbles.append(scrobble)

# fetch first page
first_page = fetch_scrobble_page(1)
append_all_scrobbles_in_page(first_page)

totalPages = int(first_page["recenttracks"]["@attr"]["totalPages"])
print "%s pages total." % (totalPages)

# fetch the rest of the pages
for i in range(2, totalPages + 1):
    # time.sleep(1)
    # API calls take over a second, so you don't need to explicitly rate limit
    # calls to one-per-second. If Last.FM gets fast, uncomment the above line.
    page = fetch_scrobble_page(i)
    append_all_scrobbles_in_page(page)

# dump it all to a json file, in case last.fm dies
all_json_file = open("all_scrobbles." + FLAGS.user + ".json", 'w')
json.dump(scrobbles, all_json_file)
all_json_file.close()


# bucketize the scrobbles according to date
scrobbles_by_date = {}
for scrobble in scrobbles:
    key = datetime.fromtimestamp(float(scrobble["date"]["uts"])).strftime("%Y-%m-%d")
    if scrobbles_by_date.has_key(key):
        scrobbles_by_date[key].append(scrobble)
    else:
        scrobbles_by_date[key] = [ scrobble ]

# print out the scrobbles in one file for each day
for date in scrobbles_by_date:
    f = codecs.open(date + "." + FLAGS.user + ".txt", 'w', 'utf8')
    for scrobble in scrobbles_by_date[date]:
        d = datetime.fromtimestamp(float(scrobble["date"]["uts"]))
        artist = scrobble["artist"]["#text"]
        album = scrobble["album"]["#text"]
        track = scrobble["name"]
        a = u"%s - %s - %s - %s\n" % (str(d), artist, album, track)
        f.write(a)
    f.close()
