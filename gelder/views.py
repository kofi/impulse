from django.shortcuts import get_object_or_404, render_to_response
from django.http import  HttpResponseRedirect #, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext #, Template, context
from django.contrib import messages
from django.conf import settings

#from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType

import hashlib

#from django.views.generic.list_detail import object_list
from sorethumb.djangothumbnail import DjangoThumbnail
from gelder.models import Record, Audio, Photo, Video

#from gelder.thumbs import  EventDisplay #RoundedCornersBackground, SmallThumb, RoundedCorners5,
#from gelder.utils import JSONResponse #api_serialize,
#from gelder.decorators import nonstaff_required
#from wall.gelder import tasks
#from wall.shortcuts import get_object_or_none

import datetime
# Create your views here.

def newaudio(request):
	"""docstring for add_event"""
	from gelder.forms import AddAudioForm
	key = 'audio'
	if request.method == 'POST':
		audio_form = AddAudioForm(request.POST, request.FILES)
		if audio_form.is_valid():
			audio = audio_form.save(commit=False)
			#audio.posted_by = request.user
			if audio_form.cleaned_data[key] is not None:
				issaved = save_file(request.FILES[key], audio_form.cleaned_data, audio, key)
				if issaved:
					messages.success(request,'Audio saved')
					return HttpResponseRedirect(reverse('gelder.views.newaudio'))
					
	 	messages.success(request, 'Audio not saved')
	else:
		audio_form = AddAudioForm()
	
	return render_to_response('gelder/newaudio.html', {'form': audio_form, }, RequestContext(request))

def newphoto(request):
	"""docstring for newphoto"""
	from gelder.forms import AddPhotoForm
	key = 'photo'
	if request.method == 'POST':
		photo_form = AddPhotoForm(request.POST, request.FILES)
		
		if photo_form.is_valid():
			photo = photo_form.save(commit=False)
			if photo_form.cleaned_data[key] is not None:
				issaved = save_file(request.FILES[key], photo_form.cleaned_data, photo, key)
				if issaved:
					messages.success(request, 'Photo saved')
					return HttpResponseRedirect(reverse('gelder.views.newphoto'))
		
		messages.success(request, 'Photo not saved')
	else:
		photo_form = AddPhotoForm()
	
	return render_to_response('gelder/newphoto.html', {'form': photo_form, }, RequestContext(request))

def newvideo(request):
	"""docstring for newphoto"""
	from gelder.forms import AddVideoForm
	key = 'video'
	issaved = False
	if request.method == 'POST':
		video_form = AddVideoForm(request.POST, request.FILES)
		if video_form.is_valid():
			video = video_form.save(commit=False)
			if video_form.cleaned_data[key] is not None:
				issaved = save_file(request.FILES[key], video_form.cleaned_data, video, key)
				if issaved:	
					messages.success(request, 'Video saved')
					return HttpResponseRedirect(reverse('gelder.views.newvideo'))
		
		messages.success(request, 'Video not saved')
	else:
		photo_form = AddVideoForm()

	return render_to_response('gelder/newvideo.html', {'form': video_form, }, RequestContext(request))

def save_file(recordfile, data, record, key):
	"""docstring for save_related_asset"""
	# try and save the asset
	asset = recordfile
	record.basename = data[key].name.replace(' ','_')
	record.filesize = data[key].size/1024
	record.caption = data['caption']
	record.filetype = data['record_contenttype']
	record.checksum = md5_for_upload(asset)
	
	# handle audio types
	if record.filetype == 'audio' : #and data['record_contenttypesub'] in ['mp3', 'mpeg', 'mpeg3']:
		record.audio = asset
		record.length = data['length']
		record.save()
	
	if record.filetype == 'image':
		record.photo = asset
		record.width = data['photowidth']
		record.height = data['photoheight']
		record.kind = data['kind']
		record.save()
		
		#if not record.save():
		#	return False
	
	if record.filetype == 'video':
		record.video = asset
		record.save()
	
	if record.id is None:
		return False
	return True		


def md5_for_upload(f):
	"""docstring for md5_for_upload"""
	md5 = hashlib.md5()
	f.open()
	for chunk in f.chunks():
		md5.update(chunk)
	return md5.hexdigest()