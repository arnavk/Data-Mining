import json
import glob
import urllib2
import pycountry

w = open('clean.txt','a')

def lookup(lat, lon):
	lat = str(lat)
	lon = str(lon)
	data = json.load(urllib2.urlopen('http://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&sensor=false' % (lat,lon)))
	for result in data['results']:
		for component in result['address_components']:
			if 'country' in component['types']:
				return component['long_name']
	return None

for files in glob.glob("*.json"):
	r = open(files,'r')
	for line in r:
		obj = json.loads(line)
		created_at = obj['created_at']
		id_str = obj['id_str']
		text = obj['text']
		user_id_str = obj['user']['id_str']
		hashtags_raw = obj['entities']['hashtags']
		hashtags = list()
		for x in range(0, len(hashtags_raw)):
			hashtags.append(hashtags_raw[x]['text'])
		if obj['geo'] != None:
			coord = obj['coordinates']['coordinates']
			coord.reverse()
		else:
			coord_raw = obj['place']['bounding_box']['coordinates']
			x1y1 = coord_raw[0][0]
			x3y3 = coord_raw[0][2]
			xx = (x3y3[0] + x1y1[0])/2
			yy = (x3y3[1] + x1y1[1])/2
			coord = [yy,xx]
		if obj['place'] != None:
			country = obj['place']['country']
			country_code = obj['place']['country_code']
		else:
			country = lookup(coord[0],coord[1])  
			input_countries = [country]
			countries = {}
			for country in pycountry.countries:
			    countries[country.name] = country.alpha2
			codes = [countries.get(country, 'Unknown code') for country in input_countries]
			country_code = codes
		lang = obj['lang']
		clean_object = [];
		clean_object.append({'created_at':created_at, 'id_str':id_str, 'text':text, 'user':user_id_str, 'hashtags':hashtags,'coord':coord,'country_code':country_code,'country':country,'lang':lang})
		new = json.dumps(clean_object)
		new_string = str(new)
		new_substring = new[1:(len(new_string)-1)]
		w.write(new_substring)
		w.write('\n')