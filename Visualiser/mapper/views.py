from django.http import HttpResponse
from django.template import RequestContext, loader

def index(request):
	template = loader.get_template('mapper/index.html')
	context = RequestContext(request, {
		'tweets': "hello",
	})
	return HttpResponse(template.render(context))