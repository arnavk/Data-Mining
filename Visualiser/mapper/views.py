from django.http import HttpResponse
from django.template import RequestContext, loader
from django.conf import settings
import os

def index(request):
	template = loader.get_template('mapper/index.html')
	tweets = open(os.path.join(settings.STATIC_ROOT, 'clean.json'), 'rb').read()
	context = RequestContext(request, {
		'tweets': tweets,
	})
	return HttpResponse(template.render(context))