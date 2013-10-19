from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.conf import settings
from mapper.models import *
import os, json

def index(request):
	template = loader.get_template('mapper/index.html')
	context = RequestContext(request)
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

def test(request):
	if request.is_ajax(): 
		post_text = request.POST.get("post_data")
		response_dict = {'response_text': '"+post_text+" recieved.'}
		print "respo"
		return HttpResponse("hello")
	else:
		return render_to_response('test.html', {},context_instance =RequestContext(request))

def initialize(request):
	r = open(os.path.join(settings.STATIC_ROOT, 'clean.json'), 'r')
	count = 0
	for line in r:
		tweetObj = json.loads(line)
		created_at = tweetObj["created_at"]
		id_str = tweetObj["id_str"]
		text = tweetObj["text"]
		user = tweetObj["user"]
		hashtags = json.dumps(tweetObj["hashtags"], ensure_ascii=False)
		coord = json.dumps(tweetObj["coord"], ensure_ascii=False)
		country_code = tweetObj["country_code"]
		country = tweetObj["country"]
		lang = tweetObj["lang"]
		tweet = Tweet(created_at = created_at, id_str = id_str, text=text, hashtags=hashtags, coord = coord, country_code = country_code, lang=lang)
		tweet.save()
		count+=1
		if count == 10000:
			print Tweet.objects.count()
			count = 0
	return index






		