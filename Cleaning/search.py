import json
import sys

# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)

search_param = sys.argv[1]
search_term = sys.argv[2]

r = open('clean.txt','r')
w = open('search.txt','w')

## special cases
if search_param == "hashtags":
	for line in r:
		tweet = json.loads(line)
		hashtag_list = tweet[search_param]
		if search_term  in hashtag_list:
			w.write(line)

## general case
elif search_param == "lang" or search_param == "country_code" or search_param == "user":
	for line in r:
		tweet = json.loads(line)
		if tweet[search_param] == search_term:
			w.write(line)
			

## rejected
else:
	print "Invalid parameters!"
	

# {"lang": "vi", "id_str": "390482740191039488", "country_code": "nil", "text": "Rrhtbk", "created_at": "Wed Oct 16 14:21:54 +0000 2013", "hashtags": [], "coord": [15.1317843, 120.9617705], "user": "280000199"}
# accepted arguments: hashtag lang country user


