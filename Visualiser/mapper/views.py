from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.conf import settings
from mapper.models import *
import os, json

def index(request):
	template = loader.get_template('mapper/index.html')
	tweets = open(os.path.join(settings.STATIC_ROOT, 'clean.json'), 'rb').read()
	context = RequestContext(request, {
		'tweets': tweets,
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
	data = open(os.path.join(settings.STATIC_ROOT, 'smaller_clean.json'))
	tweets = json.load(data)
	print tweets[2]["lang"]
	print str(json.dumps(tweets))
	return HttpResponse(json.dumps(tweets, ensure_ascii=False))

def test(request):
	if request.is_ajax(): 
		post_text = request.POST.get("post_data")
		response_dict = {'response_text': '"+post_text+" recieved.'}
		print "respo"
		return HttpResponse("hello")
	else:
		return render_to_response('test.html', {},context_instance =RequestContext(request))