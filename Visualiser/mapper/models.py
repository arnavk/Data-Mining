from django.db import models
from django import forms
import json

class Tweet (models.Model):
	created_at = models.TextField()
	id_str = models.TextField()
	text = models.TextField()
	# user = models.TextField()
	hashtags = models.TextField(null=True)
	coord = models.TextField(null=True)
	country_code = models.TextField(null=True)
	country = models.TextField(null=True)
	lang = models.TextField(null=True)
	def jsonize(self):
		# TODO - CHECK!!
		tweet = {}
		tweet['created_at'] = self.created_at
		tweet['id_str'] = self.id_str
		tweet['text'] = self.text
		# tweet['user'] = self.user
		tweet['hashtags'] = self.hashtags
		tweet['coord'] = self.coord
		tweet['country_code'] = self.country_code
		tweet['country'] = self.country
		tweet['lang'] = self.lang
		return json.dumps(tweet, ensure_ascii=False)
	def dictize(self):
		tweet = {}
		tweet['created_at'] = self.created_at
		tweet['id_str'] = self.id_str
		tweet['text'] = self.text
		# tweet['user'] = self.user
		tweet['hashtags'] = json.loads(self.hashtags)
		tweet['coord'] = json.loads(self.coord)
		tweet['country_code'] = self.country_code
		tweet['country'] = self.country
		tweet['lang'] = self.lang
		return tweet