from django.db import models

from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

# contenttype 
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from impulse.gelder.models import Audio, Video, Photo

# Create your models here.
class Artist(models.Model):
	"""(Artist description)"""
	name = models.CharField(blank=True, max_length=100)
	photo = generic.GenericRelation(Photo)
	audio = generic.GenericRelation(Audio)
	video = generic.GenericRelation(Video)
	
	def __unicode__(self):
		return self.name
	
	
