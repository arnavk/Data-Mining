from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.conf import settings
from mapper.models import *
import os, json

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
	# if range == "all":
	clusters = open(os.path.join(settings.STATIC_ROOT, 'clustered.json'), 'rb').read()
	print clusters
	clusterJSON = json.loads(clusters)
	print clusterJSON[1]
	return HttpResponse(json.dumps(clusterJSON, ensure_ascii=False))
	# else:
	# 	print range

def startTime():
	return "Tue Oct 22 13:52:24 +0000 2013"

def endTime():
	return "Wed Oct 23 21:53:13 +0000 2013"

def compareTo(time1, time2):
	formattedTime1 = time1[time1.find(" "):]
	formattedTime2 = time2[time2.find(" "):]
	return cmp(formattedTime1, formattedTime2)
