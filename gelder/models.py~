import uuid
from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

# contenttype 
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

#django contrib
from django.contrib.auth.models import User

#django utils
from django.utils.encoding import smart_str
from django.template.defaultfilters import slugify

#python
import datetime, os

from mutagen.easyid3 import EasyID3

#from wall.gelder import tasks
from sorethumb.djangothumbnail import DjangoThumbnail
from thumbs import EventDisplay

class OwnerAssetManager(object):
	"""docstring for OwnerAssetManager"""
	def get_query_set(self):
		"""docstring for get_query_set"""
		return super(OwnerAssetManager, self).get_query_set()

	
class ActiveAssetManager(models.Manager):
	"""docstring for PhotoManager"""
	#use_for_related_fields = True
	def get_query_set(self):
		return super(ActiveAssetManager, self).get_query_set().filter(state=Record.ACTIVE_STATUS)

	

# Create your models here.
class Record(models.Model):
	""" Class defines base object for Model assets"""
	
	ACTIVE_STATUS= 1
	DELETE_STATUS=0
	STATE_CHOICES = (
		(ACTIVE_STATUS,'Active'),
		(DELETE_STATUS,'Deleted'),
	)	
	AUDIOTYPE = u'Audio'
	PHOTOTYPE = u'Photo'
	VIDEOTYPE = u'Video'
	RECORD_TYPES = (
		(AUDIOTYPE,'Audio'),
		(PHOTOTYPE,'Photo'),
		(VIDEOTYPE,'Video'),
	)
	
	
	uuid = models.CharField(blank=False, max_length=32)
	filetype = models.CharField(blank=False, max_length=32)
	recordtype = models.CharField(choices=RECORD_TYPES, default=AUDIOTYPE, max_length=32)
	#event = models.ForeignKey(Event, blank=True)
	checksum = models.CharField(blank=False, max_length=255)
	basename = models.CharField(blank=False, max_length=100)
	filesize = models.IntegerField(blank=False, null=False)
	added = models.DateTimeField(blank=False, default=datetime.datetime.now)
	state = models.IntegerField(choices=STATE_CHOICES, default=ACTIVE_STATUS,)
	caption = models.CharField(blank=True, max_length=100)
	url = models.URLField(blank=True, verify_exists=True)
	uploaded = models.BooleanField(default=False,)
	uploaddate = models.DateTimeField(blank=True,default=datetime.datetime.now)
	
	
	# create the foreignkey to handle the generic foreigney
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type', 'object_id')
    # handle the object managers
	objects= ActiveAssetManager()	
	allobjects = models.Manager()
		
	class Meta:
		abstract = True
		ordering = ['added']
		unique_together = ('content_type', 'object_id')
	
	
	def save(self, *args, **kwargs):
		"""docstring for save"""
		#self.uploaded = datetime.datetime.now()
		#self.url = 'http://' + settings.S3_AUDIOART_BUCKET + '.s3.amazonaws.com/' + self.url
		self.save()
		#super(Record, self).save(*args, **kwargs)
	
	def checkurl(self, url):
		"""docstring for checkurl"""
		if not url:
			return False
		validate = URLValidator(verify_exists=True)
		try:
			validate(url)
			return True
		except ValidationError, e:
			return False
	
	def getUUID(self):
		"""docstring for getUUID"""
		return str(uuid.uuid4().hex)
	
	def get_absolute_url(self):
		"""docstring for get_absolute_url"""
		# if settings.GELDER_MEDIA_FILESERVER == 'aws':
		# 	if self.checkurl(self.get_audio_url()):
		# 		return self.get_audio_url()
		if self.uploaded is True : #and self.checkurl(self.get_web_url()):  #self.url):
			return self.get_web_url()  
		return self.get_local_url()
	
	def get_web_url(self):
		"""docstring for get_web_url"""
		#return "%s" % (self.url)
		# au = self.audiourl_set.all()
		# if au and au.count() and self.checkurl(au[0].url):
		# 	return au[0].url
		if self.recordtype == self.PHOTOTYPE:
			url = "http://%s.s3.amazonaws.com/%s" % (settings.GELDER_S3_PHOTO_BUCKET,self.basename)
		if self.recordtype == self.AUDIOTYPE:
			url = "http://%s.s3.amazonaws.com/%s" % (settings.GELDER_S3_AUDIO_BUCKET,self.basename)
		if self.recordtype == self.VIDEOTYPE:
			url = "http://%s.s3.amazonaws.com/%s" % (settings.GELDER_S3_VIDEO_BUCKET,self.basename)		
		
		return url
		# if self.checkurl(url):
		# 	return url
		# return self.get_local_url()
	
	def get_s3_bucket(self, bucketname = None):
		"""docstring for get_s3_bucket"""
		if not bucketname:
			bucketname = type(self).__name__.lower()
		buckets = {
			'photo' : settings.GELDER_S3_PHOTO_BUCKET, 
			'audio' : settings.GELDER_S3_AUDIO_BUCKET,
			'audioart' : settings.S3_AUDIOART_BUCKET,
			'video' : settings.GELDER_S3_VIDEO_BUCKET,
			'event_display': settings.S3_PHOTO_DISPLAY_BUCKET, 
			'small_thumb': settings.S3_PHOTO_THUMB_BUCKET,
		}
		return buckets.get(bucketname, None) 
	
	def filesize_in_Mb(self):
		"""docstring for filesize_in_Kb"""
		return float(self.filesize)/1024
	filesize_in_Mb.short_description = 'Filesize (Mb)'
	filesize_in_Mb.admin_order_field = 'filesize'
	


class Photo(Record):
	"""docstring for Photo"""
	PHOTO_TYPES = (
		('audioart','AlbumArt'),
		('generic','Generic'),
	)	
	FILE_TYPES = ['jpeg', 'jpg', 'png']
	MAX_SIZE = 7*1024*1024
	local_uploadto = getattr(settings, 'GELDER_LOCAL_PHOTO_UPLOADTO', None)
	
	photo = models.FileField(upload_to= local_uploadto) #'%Y_%m_%d_%H')
	kind = models.CharField(blank=False,choices = PHOTO_TYPES, max_length=15)
	height = models.IntegerField(blank=True)
	width = models.IntegerField(blank=True)
	
	def __unicode__(self):
		"""docstring for __unicode__"""
		return self.caption
	
	def save(self, *args, **kwargs):
		"""docstring for save"""
		# only generate a uuid if none does not yet exist 
		self.recordtype = self.PHOTOTYPE
		if not self.uuid:
			self.uuid = self.getUUID()
		ext = self.basename.rpartition(".")
		#raise Exception([self.basename, self.photo.url, self.photo.name, self.photo.path, self.photo,])
		self.basename = self.uuid + "." +self.basename.rpartition(".")[2]
		self.photo.name = self.local_uploadto + self.basename
		super(Record, self).save(*args, **kwargs)
	
	def get_local_url(self):
		"""docstring for get_local_url"""
		return "%s" % (self.photo.url)
	
	def generate_photo_thumb(self, format='small_thumb'):
		"""docstring for generate_photo_thumb"""
		#import re
		thumbtag = {'event_display': settings.GELDER_PHOTO_DISPLAY_TAG, 
					'small_thumb': settings.GELDER_PHOTO_THUMB_TAG 	}
		thumb = DjangoThumbnail.render(format, self.photo.path)
		# isolate unique hash generated by Django thumbnail
		djunique = thumb.replace('/'+self.photo.name+'.thumb.png','').replace(settings.SORETHUMB_URL_ROOT,'')
		# generate the new photo/thumbnail name
		newthumb = '%s/%s/%s/%s%s.%s%s' % (settings.SORETHUMB_OUTPUT_PATH, djunique, self.photo.name.replace(self.basename,''),
					 		thumbtag[format], self.basename.rpartition('.')[0], thumbtag[format], '.png')
		newthumb = os.path.normpath(newthumb)
		if os.path.isfile(newthumb):
			return newthumb
		
		thumb = os.path.normpath(os.path.join(settings.SORETHUMB_OUTPUT_PATH, thumb.replace(settings.SORETHUMB_URL_ROOT,'')))
		if not os.path.isfile(thumb): 
			return False
		
		os.rename(thumb, newthumb)
		if not os.path.isfile(newthumb): 
			return False		
		return newthumb
	
	def photo_dimensions(self):
		"""docstring for photo_dimensions"""
		return "%s x %s" % (self.width, self.height)
	photo_dimensions.short_description = 'Dimensions'
	photo_dimensions.admin_order_field = 'width'

	

class Video(Record):
	"""docstring for Video"""
	FILE_TYPES = ['mp4','flv','avi','m4v']
	MAX_SIZE = 50*1024*1024
	local_uploadto = getattr(settings, 'GELDER_LOCAL_VIDEO_UPLOADTO', None)
	video = models.FileField(upload_to= local_uploadto)  #'%Y_%m_%d_%H')
	
	def __unicode__(self):
		"""docstring for __unicode__"""
		return self.caption
	
	def save(self, *args, **kwargs):
		"""docstring for save"""
		self.recordtype = self.VIDEOTYPE
		if not self.uuid:
			self.uuid = self.getUUID()
		self.basename = self.uuid + "." +self.basename.rpartition(".")[2]
		self.video.name = self.local_uploadto + self.basename
		super(Record, self).save(*args, **kwargs)
	
	def get_local_url(self):
		"""docstring for get_local_url"""
		return "%s" % (self.video.url)	
	

class Audio(Record):
	"""docstring for Photo"""
	FILE_TYPES = ['mp3', 'mpeg', 'mpeg3',]
	MAX_SIZE = 10*1024*1024
	local_uploadto = getattr(settings, 'GELDER_LOCAL_AUDIO_UPLOADTO', None)
	
	audio = models.FileField(upload_to= local_uploadto) #'%Y_%m_%d_%H') #
	length = models.IntegerField(blank=True)
		
	def __unicode__(self):
		return self.caption
	
	def save(self, *args, **kwargs):
		"""docstring for save"""
		self.recordtype = self.AUDIOTYPE
		# get the uuid
		if not self.uuid:
			self.uuid = self.getUUID()
		# change the basename
		self.basename = self.uuid + "." +self.basename.rpartition(".")[2]
		# ... then change the file name
		self.audio.name = self.local_uploadto + self.basename
		super(Record, self).save(*args, **kwargs)
	
	# def get_absolute_url(self):
	# 	"""docstring for get_absolute_url"""
	# 	if settings.GELDER_MEDIA_FILESERVER == 'aws':
	# 		if self.checkurl(self.get_audio_url()):
	# 			return self.get_audio_url()
	# 	return self.get_local_url()
	# 
	# def get_audio_url(self):
	# 	"""docstring for get_audio_url"""
	# 	au = self.audiourl_set.all()
	# 	if au and au.count() and self.checkurl(au[0].url):
	# 		return au[0].url
	# 	url = "http://%s.s3.amazonaws.com/%s" % (settings.GELDER_S3_AUDIO_BUCKET,self.basename)
	# 	if self.checkurl(url):
	# 		return url
	# 	return self.get_local_url()
	def get_local_url(self):
		"""docstring for get_local_url"""
		return "%s" % (self.audio.url)
	
	def audio_length(self):
		"""docstring for audio_length"""
		l = '%s' % (self.length/60.0, )
		u = l.split('.')
		return "%s:%s" % (u[0], u[1],)
	audio_length.short_description = 'Length'
	audio_length.admin_order_field = 'length'
	
	def audio_artist(self):
		"""docstring for audio_artist"""
		song = EasyID3(self.audio.path)
		if not song.has_key('artist'):
			return 'Unknown'
		return song['artist'][0]
	audio_artist.short_description = 'Artist'
	audio_artist.admin_order_field = 'artist'
	
	def audio_title(self):
		"""docstring for audio_title"""
		song = EasyID3(self.audio.path)
		if not song.has_key('title'):
			return 'Unknown'
		return song['title'][0]
	audio_title.short_description = 'Title'
	audio_title.admin_order_field = 'title'
	
	def audio_genre(self):
		"""docstring for audio_title"""
		song = EasyID3(self.audio.path)
		if not song.has_key('genre'):
			return 'Unknown'
		return song['genre'][0]
	audio_genre.short_description = 'Genre'
	audio_genre.admin_order_field = 'genre'
	
	

	
# SIGNALS
def delete_media_from_s3(sender, **kwargs):
	"""docstring for delete_from_s3"""
	obj = kwargs['instance']
	from gelder.tasks import delete_from_s3
	if type(obj).__name__ == 'Photo':
		# find a way to reset uploaded property to false
		#if os.path.isfile(obj.photo.path) == True:
		#	os.remove(obj.photo.path)
		delete_from_s3.delay(obj.basename, settings.GELDER_S3_PHOTO_BUCKET)
		# delete the thumb
		delete_from_s3.delay('thumb_' + obj.basename, settings.GELDER_S3_PHOTO_BUCKET)
		# then delete the displays
		delete_from_s3.delay('display_' + obj.basename, settings.GELDER_S3_PHOTO_BUCKET)
	if type(obj).__name__ == 'Audio':
		delete_from_s3.delay(obj.basename, settings.GELDER_S3_AUDIO_BUCKET)
	if type(obj).__name__ == 'Video':
		delete_from_s3.delay(obj.basename, settings.GELDER_S3_VIDEO_BUCKET)

post_delete.connect(delete_media_from_s3,sender=Audio,)
post_delete.connect(delete_media_from_s3,sender=Photo,)
post_delete.connect(delete_media_from_s3,sender=Video,)

def upload_media_to_s3(sender, **kwargs):
	"""docstring for delete_from_s3"""
	obj = kwargs['instance']
	#from gelder.tasks import upload_to_s3
	if type(obj).__name__ == 'Photo':
		upload_photo(sender, **kwargs)
		#upload_to_s3.delay(obj.photo.basename, settings.GELDER_S3_PHOTO_BUCKET)
	if type(obj).__name__ == 'Audio':
		upload_audio(sender, **kwargs)
		#upload_to_s3.delay(obj.audio.basename, settings.GELDER_S3_AUDIO_BUCKET)
	if type(obj).__name__ == 'Video':
		upload_video(sender, **kwargs)
		#upload_to_s3.delay(obj.audio.basename, settings.GELDER_S3_VIDEO_BUCKET)

post_save.connect(upload_media_to_s3,sender=Audio,)
post_save.connect(upload_media_to_s3,sender=Photo, dispatch_uid="gelder_photo_save")
post_save.connect(upload_media_to_s3,sender=Video,)


def upload_photo(sender, **kwargs):
	"""docstring for upload_photo_to_s3"""
	obj = kwargs['instance']
	mname = type(obj).__name__
	if mname == 'Photo': 
		if obj.uploaded == False:
			from gelder.tasks import upload_photo_to_s3_task
			upload_photo_to_s3_task.delay(obj.id, model=mname)

#post_save.connect(upload_photo,sender=Photo,)
#post_save.connect(upload_photo,sender=AudioArtUrl,)

def upload_audio(sender, **kwargs):
	"""docstring for upload_audio_to_s3"""
	obj = kwargs['instance']
	if type(obj).__name__ == 'Audio':
		if obj.uploaded == False:
			from gelder.tasks import upload_audio_to_s3
			upload_audio_to_s3.delay(obj.id)

#post_save.connect(upload_audio, sender=Audio,)

def upload_video(sender, **kwargs):
	"""docstring for upload_video"""
	obj = kwargs['instance']
	if type(obj).__name__ == 'Video':
		if obj.uploaded == False:
			vimeo_quota = obj.check_vimeo_quota()
			if vimeo_quota > obj.filesize/1024: 	
				from gelder.tasks import upload_video_to_vimeo
				upload_video_to_vimeo.delay(obj.id,)
			else:
				from gelder.tasks import upload_video_to_youtube
				upload_video_to_youtube.delay(obj.id,)
			from gelder.tasks import upload_video_to_s3
			upload_video_to_s3.delay(obj.id)

#post_save.connect(upload_video,sender=Video,)


