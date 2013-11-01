from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.conf import settings
from mapper.models import *
import os, json, operator
from dbscan import *

def index(request):
	template = loader.get_template('mapper/index.html')
	context = RequestContext(request, {
		'startTime': startTime,
		'endTime' : endTime,
	})
	return HttpResponse(template.render(context))

def search(request):
	if request.method == 'POST': # If the form has been submitted...
		form = SearchForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			hashtag = form.cleaned_data["hashtag"]
			return HttpResponse("searching for " + hashtag)
	else:
		form = SearchForm() # An unbound form

	return index

def tagsearch(request, hashtag):
	print hashtag
	# data = open(os.path.join(settings.STATIC_ROOT, 'smaller_clean.json'), 'rb').read()
	tweets = Tweet.objects.exclude(hashtags="[]")
	filteredTweets = []
	for tweet in tweets:
		hashtags = json.loads(tweet.hashtags)
		for usedHashtag in hashtags:
			if hashtag.lower() == usedHashtag.lower():
				filteredTweets.append(tweet.dictize())
	return HttpResponse(json.dumps(filteredTweets, ensure_ascii=False))

def initialize(request):
	r = open(os.path.join(settings.STATIC_ROOT, 'final_data.json'), 'r')
	count = 0
	for line in r:
		tweetObj = json.loads(line)
		created_at = tweetObj["created_at"]
		id_str = tweetObj["id_str"]
		text = tweetObj["text"]
		user_handle = tweetObj["user_handle"]
		user_id = tweetObj["user_id"]
		hashtags = json.dumps(tweetObj["hashtags"], ensure_ascii=False)
		coord = json.dumps(tweetObj["coord"], ensure_ascii=False)
		country_code = tweetObj["country_code"]
		country = tweetObj["country"]
		lang = tweetObj["lang"]
		tweet = Tweet(created_at = created_at, id_str = id_str, text=text, user_id=user_id, user_handle=user_handle,  hashtags=hashtags, coord = coord, country_code = country_code, lang=lang)
		tweet.save()
		count+=1
		if count == 10000:
			print Tweet.objects.count()
			count = 0
	return index

def clusters (request, range):
	if range == "all":
		clusters = open(os.path.join(settings.STATIC_ROOT, 'clustered.json'), 'rb').read()
		print clusters
		clusterJSON = json.loads(clusters)
		print clusterJSON[1]
		return HttpResponse(json.dumps(clusterJSON, ensure_ascii=False))
	else:
		rangeArray = range.split("|")
		start = rangeArray[0]
		end = rangeArray[1]
		print start
		print end
		tweets = Tweet.objects.exclude(hashtags="[]")
		filteredTweets = []
		hashtagCountMap = {}
		for tweet in tweets:
			time = tweet.javascriptTime()
			#print "Tweet time: " + time 
			if (compareTo(start, time) <= 0) and (compareTo(time, end) <= 0):
				filteredTweets.append(tweet.dictize())
				hashtags = json.loads(tweet.hashtags)
				for usedHashtag in hashtags:
					if usedHashtag in hashtagCountMap:
						hashtagCountMap[usedHashtag] += 1
					else:
						hashtagCountMap[usedHashtag] = 1
		#print len(filteredTweets)
		sortedMap = sorted(hashtagCountMap.iteritems(), key=operator.itemgetter(1), reverse=True)
		# print "printing sortedMap"
		# print sortedMap
		commonHashtags = []
		hashtagMap = {}
		for hashtag in sortedMap[:10]:
			commonHashtags.append(hashtag[0])
			hashtagMap[hashtag[0]] = []
			print hashtag[0]
		tweets = filteredTweets
		for tweet in tweets:
			#print tweet
			hashtags = tweet["hashtags"]
			for usedHashtag in hashtags:
				if usedHashtag in commonHashtags:
					hashtagMap[usedHashtag].append(tweet)
		print commonHashtags
		clusters = []
		for hashtag in commonHashtags: 
			clustersForTag = clusterForTag(hashtagMap[hashtag])
			for cluster in clustersForTag:
				cluster["hashtag"] = hashtag
				clusters.append(cluster)
				print cluster
		#clusters = open(os.path.join(settings.STATIC_ROOT, 'clustered2.json'), 'rb').read()
		# clusterJSON = clusters
		return HttpResponse(json.dumps(clusters, ensure_ascii=False))


def startTime():
	return "Tue Oct 22 13:52:24 +0000 2013"
# "Wed Oct 23 2013 07:28:38 GMT+0800 (SGT)"
def endTime():
	return "Wed Oct 23 21:53:13 +0000 2013"

def compareTo(time1, time2):
	time1array = time1.split()
	time2array = time2.split()
	formattedTime1 = time1array[1] + " " + time1array[2] + " " + time1array[3] + " " + time1array[4]
	formattedTime2 = time2array[1] + " " + time2array[2] + " " + time2array[3] + " " + time2array[4]
	#print formattedTime1 + " " + formattedTime2
	#print cmp(formattedTime1, formattedTime2)
	return cmp(formattedTime1, formattedTime2)

def clusterForTag(tweets):
	dbscan = DBSCAN()
	dbscanList = []
	for tweet in tweets:
		coord = tweet['coord']
		p = Point(coord[0], coord[1])
		dbscanList.append(p)
	clusterSet = []
	dbscan.DB = dbscanList
	clusterSet = dbscan.DBSCAN()
	
	for cluster in clusterSet:
		print "Centroid:", cluster['centroid'], ", Size: ", cluster['size']
	return clusterSet
