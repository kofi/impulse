from django import forms
from django.forms import ModelForm
from django.forms import extras
from django.core.files.images import get_image_dimensions
#from django.forms.extras.widgets import SelectDateWidget

from models import Record, Audio, Photo, Video #, AudioArt, Photo #, Asset, Photo
#from widgets import SelectTimeWidget #, SelectDateFilterWidget
#from selectdatewidget import SelectDateWidget

import datetime
import magic #http://stackoverflow.com/questions/43580/how-to-find-the-mime-type-of-a-file-in-python
import hashlib


def md5_for_upload(f):
	"""docstring for md5_for_upload"""
	md5 = hashlib.md5()
	f.open()
	for chunk in f.chunks():
		md5.update(chunk)
	return md5.hexdigest()

def validate_file_size(data, key, maxsize=12*1024*1024):
	"""docstring for validate_file_size"""
	#raise Exception([data, data[key].size])
	if data[key].size > maxsize:
		return False
	return True

def validate_image_size(data, key, maxwidth=1200, maxheight=1200):
	"""docstring for validate_image"""
	w, h = get_image_dimensions(data['key'])
	if w > maxwidth or h > maxheight:
		return False
	return True

def validate_image_type(data,key,):
	"""docstring for validate_image_type"""
	mtype_main, mtype_sub, ctype_main, ctype_sub = get_file_type(data, key)
	if ctype_main != 'image':
		return False
	if mtype_main != ctype_main or mtype_sub != ctype_sub:
		return False
	if ctype_sub not in ['jpeg', 'jpg', 'png']:
		return False
	return (True, ctype_main, ctype_sub, )

def validate_upload_type(data, key, checktype):
	"""docstring for validate_upload_type"""
	mtype_main, mtype_sub, ctype_main, ctype_sub = get_file_type(data, key)
	#raise 
	# if ctype_main != checktype:
	# 	return (False, ctype_main, ctype_sub )
	if ctype_main != 'audio':
		if mtype_main != ctype_main or mtype_sub != ctype_sub:
			return (False, ctype_main, ctype_sub, )
	if checktype == 'image':
		if ctype_main != checktype:
			return (False, ctype_main, ctype_sub, )
		if ctype_sub not in ['jpeg', 'jpg', 'png']:
	 		return (False, ctype_main, ctype_sub, )
	if checktype == 'audio':
		if ctype_sub not in ['mp3', 'm4a', 'mpeg', 'mpeg3']:
			return (False, ctype_main, ctype_sub,)
	return (True, ctype_main, ctype_sub, )	

		
def get_file_type(data,key):
	"""docstring for getuploadtype"""
	mime = magic.Magic(mime=True) 
	filemime = mime.from_file(data[key].temporary_file_path())
	mtype_main, mtype_sub = filemime.split('/')
	ctype_main, ctype_sub = data[key].content_type.split('/')
	
	return (mtype_main, mtype_sub, ctype_main, ctype_sub )


class AddVideoForm(ModelForm):
	"""docstring for AddPhotoForm"""
	def __init__(self, *args, **kwargs):
		exkey = 'exclude_list'
		exclude_list = []
		if exkey in kwargs:
			exclude_list=kwargs[exkey]
			del kwargs[exkey]
		super(AddVideoForm, self).__init__(*args, **kwargs)
		for field in exclude_list:
			del self.fields[field]
				
	class Meta:
		"""docstring for Meta"""
		model = Video
		exclude = ['uuid','filetype','recordtype', 'basename', 'checksum','state','url',
		 	'added', 'filesize', 'uploaded', 'uploaddate', 'length', 'content_type','object_id']
	
	def clean(self):
		"""docstring for clean"""
		if 'video' not in self.cleaned_data:
			msg = u'Please upload a video file'
			self._errors['video'] = self.error_class([msg])
			raise forms.ValidationError(msg)
		else:
			isvalid, ctype_main, ctype_sub = validate_upload_type(self.cleaned_data, 'video', 'video')
			if isvalid !=True:
				msg =u'Invalid image file submitted'
				self._errors['video'] = self.error_class([msg])
				raise forms.ValidationError(msg)

			self.cleaned_data['record_contenttype'] = ctype_main
			self.cleaned_data['record_contenttypesub'] = ctype_sub

			self.c_record_video()

		return self.cleaned_data
	

	def c_record_video(self,):
		"""docstring for c_asset_photo"""
		if self.cleaned_data['record_contenttype'] == 'video' and \
			self.cleaned_data['record_contenttypesub'] not in Video.FILE_TYPES:
			msg = 'Invalid video type. Video should be in mp4, flv, avi or m4v format.'
			self._errors['video'] = self.error_class([msg])
			raise forms.ValidationError(msg)

		isgoodsize = validate_file_size(self.cleaned_data, 'video', Video.MAX_SIZE)
		if isgoodsize == False:
			msg = u'Video size must be less than %s Mb' % Video.MAX_SIZE/(1024*1024)
			self._errors['video'] = self.error_class([msg])
			raise forms.ValidationError(msg)

		return True
	


class AddPhotoForm(ModelForm):
	"""docstring for AddPhotoForm"""
	def __init__(self, *args, **kwargs):
		exkey = 'exclude_list'
		exclude_list = []
		if exkey in kwargs:
			exclude_list= kwargs[exkey]
			del kwargs[exkey]
		super(AddPhotoForm, self).__init__(*args, **kwargs)
		for field in exclude_list:
			del self.fields[field]
	
	class Meta:
		"""docstring for Meta"""
		model = Photo
		exclude = ['uuid','filetype','recordtype', 'basename', 'width', 'height', 'checksum',
			'state','url', 'added', 'filesize', 'uploaded', 'uploaddate', 'length', 'content_type','object_id']
	
	def clean(self):
		"""docstring for clean"""
		if 'photo' not in self.cleaned_data:
			msg = u'Please upload an image file'
			self._errors['photo'] = self.error_class([msg])
			raise forms.ValidationError(msg)
		else:
			isvalid, ctype_main, ctype_sub = validate_upload_type(self.cleaned_data, 'photo', 'image')
			if isvalid !=True:
				msg = u'Invalid image file submitted'
				self._errors['photo'] = self.error_class([msg])
				raise forms.ValidationError(msg)

			self.cleaned_data['record_contenttype'] = ctype_main
			self.cleaned_data['record_contenttypesub'] = ctype_sub
			
			isgoodsize = validate_file_size(self.cleaned_data, 'photo', Photo.MAX_SIZE)
			if isgoodsize == False:
				msg = u'Photo size must be less than %s Mb' % Photo.MAX_SIZE/1024/1024
				self._errors['photo'] = self.error_class([msg])
				raise forms.ValidationError(msg)
			
			self.c_record_photo()

		return self.cleaned_data
	
		
	def c_record_photo(self,):
		"""docstring for c_asset_photo"""
		max_width = 1200
		max_height = 1200
		if self.cleaned_data['record_contenttype'] == 'image' and self.cleaned_data['record_contenttypesub'] not in Photo.FILE_TYPES:
			msg = u'Invalid image type. Picture should be in jpeg, jpg, png formats.'
			self._errors['photo'] = self.error_class([msg])
			raise forms.ValidationError(msg)
		photo = self.cleaned_data['photo']
		w, h = get_image_dimensions(photo)

		if w > max_width or h > max_height:
			msg = u'Max image dimensions %sx%s pixels' % (max_width,max_height)
			self._errors['photo'] = self.error_class([msg])
			raise forms.ValidationError(msg)
		self.cleaned_data['photowidth'] = w
		self.cleaned_data['photoheight'] = h

		return True
	
	
class AddAudioForm(ModelForm):   
	"""docstring for AddAudioForm"""
	def __init__(self, *args, **kwargs):
		exkey = 'exclude_list'
		exclude_list = []
		if exkey in kwargs:
			exclude_list=kwargs[exkey]
			del kwargs[exkey]
		super(AddAudioForm, self).__init__(*args, **kwargs)
		for field in exclude_list:
			del self.fields[field]
	
	class Meta:
		"""docstring for Meta"""
		model = Audio
		exclude = ['uuid','filetype','recordtype', 'basename', 'checksum','state','url', 'added', 
				'filesize', 'uploaded', 'uploaddate', 'length', 'content_type','object_id']
	
	# http://oranlooney.com/django-file-uploads/
	def clean(self):
		"""clean the attached asset/image(s)"""
		if 'audio' not in self.cleaned_data:  #self.cleaned_data['audio'] is None:
			msg = u'Please upload an audio file'
			self._errors['audio'] = self.error_class([msg])
			raise forms.ValidationError(msg)
			#pass
		else:
			
			isvalid, ctype_main, ctype_sub = validate_upload_type(self.cleaned_data, 'audio', 'audio')
			if isvalid != True:
				msg = u'Invalid file type submitted'
				self._errors['audio'] = self.error_class([msg])
				raise forms.ValidationError(msg)
				
			self.cleaned_data['record_contenttype'] = ctype_main
			self.cleaned_data['record_contenttypesub'] = ctype_sub
		
			isgoodsize = validate_file_size(self.cleaned_data, 'audio', Audio.MAX_SIZE)
			if isgoodsize == False:
				msg = u'Audio size must be less than %s Mb' % Audio.MAX_SIZE/(1024*1024)
				self._errors['audio'] = self.error_class([msg])
				raise forms.ValidationError(msg)

			self.c_record_audio()

		return self.cleaned_data
	
	def c_record_audio(self,):
		"""docstring for c_asset_audio"""
		#raise Exception([self.cleaned_data['asset_contenttype'], self.cleaned_data['asset_contenttypesub']  ])
		
		keys_to_extract = ['artist','title','length']
		if self.cleaned_data['record_contenttype'] == 'audio' and self.cleaned_data['record_contenttypesub'] not in Audio.FILE_TYPES:
			msg =u'Invalid audio type. Audio file should be in mp3 format.'
			self._errors['audio'] = self.error_class([msg])
			raise forms.ValidationError(msg)
			
		if self.cleaned_data['record_contenttypesub'] in Audio.FILE_TYPES :
			self.cleaned_data['length'] = 10
			from mutagen.easyid3 import EasyID3
			audio = self.cleaned_data['audio']
			song = EasyID3(audio.temporary_file_path())
			if not song:
				msg = u'Could not upload the audio file you submitted'
				self._errors['audio'] = self.error_class([msg])
				raise forms.ValidationError(msg)

			if not song.has_key('artist') or not song.has_key('title'):
				msg = u'Song should have following at least following tags: title, artist, length'
				self._errors['audio'] = self.error_class([msg])
				raise forms.ValidationError(msg)
				
			from mutagen.mp3 import MP3
			au = MP3(audio.temporary_file_path())
			#### to extract artist:au['TPE1'].text[0], title: au['TIT2'].text[0], album: au['TALB'].text[0]
			if au.info.length:
				self.cleaned_data['length'] = au.info.length
			else:
				self.cleaned_data['length'] = 10000
				msg = u'Could not get the length of the song. Please edit your song tags'
				self._errors['audio'] = self.error_class([msg])
				raise forms.ValidationError(msg)

		return True
	
	
	
		

