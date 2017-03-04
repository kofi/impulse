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

from django.forms.models import inlineformset_factory

import hashlib

#from django.views.generic.list_detail import object_list
from sorethumb.djangothumbnail import DjangoThumbnail
from juno.models import Artist
from gelder.forms import AddVideoForm, AddAudioForm, AddPhotoForm
from gelder.models import Photo, Audio, Video

#from gelder.thumbs import  EventDisplay #RoundedCornersBackground, SmallThumb, RoundedCorners5,
#from gelder.utils import JSONResponse #api_serialize,
#from gelder.decorators import nonstaff_required
#from wall.gelder import tasks
#from wall.shortcuts import get_object_or_none

import datetime
# Create your views here.

def aindex(request, name):
	"""docstring for event_detail"""
	artist = get_object_or_404(Artist, name=name)
	#event_asset = event.get_asset()
	#assets = event_asset['asset'] ##Photo.objects.filter(event=event.id) or None
	#category = Category.objects.filter(id=event.category.id) or None
	#if category is not None:
	#	event.categoryname = category[0].name
	#	categoryname = category[0].name
	#return render_to_response('gelder/event_detail.html', {'event': event, 'asset_json': assets[0], 'asset_object':assets[0], 
	#		'categoryname':categoryname}, RequestContext(request))
	return render_to_response('juno/artistindex.html', {'artist': artist, }, RequestContext(request))

def newartist(request):
	"""docstring for add_event"""
	from juno.forms import AddArtistForm
	key = 'artist'
	if request.method == 'POST':
		artist_form = AddArtistForm(request.POST, request.FILES)
		if artist_form.is_valid():
			artist = artist_form.save(commit=True)
			#audio.posted_by = request.user
			# if artist_form.cleaned_data[key] is not None:
			# 	issaved = save_file(request.FILES[key], audio_form.cleaned_data, audio, key)
			# 	if issaved:
			messages.success(request,'Artist saved')
			return HttpResponseRedirect(reverse('juno.views.newartist'))
					
	 	messages.success(request, 'Artist not saved')
	else:
		artist_form = AddArtistForm()
	
	return render_to_response('juno/newartist.html', {'form': artist_form, }, RequestContext(request))


def newartistphoto(request):
	"""docstring for add_event"""
	from juno.forms import AddArtistForm
	from gelder.views import save_file
	key = 'artist'
	recordkey = 'photo'
	if request.method == 'POST':
		artist_form = AddArtistForm(request.POST)
		photo_form = AddPhotoForm(request.POST, request.FILES)
		if artist_form.is_valid() and photo_form.is_valid():
			newartist = artist_form.save(commit=True)
			newphoto = photo_form.save(commit=False)
			newphoto.content_object = newartist
			#raise Exception([newphoto.basename, newphoto.photo.name, newphoto.photo.path, newphoto.photo,])
			
			if photo_form.cleaned_data[recordkey] is not None:
				issaved = save_file(request.FILES[recordkey], photo_form.cleaned_data, newphoto, recordkey)
				if not issaved:
					messages.success(request, 'Photo not saved')
					return HttpResponseRedirect(reverse('juno.views.newartistphoto'))
			
			newphoto.save()
			messages.success(request,'Artist saved')
			return HttpResponseRedirect(reverse('juno.views.newartistphoto'))
		# 	#audio.posted_by = request.user
		# 	# if artist_form.cleaned_data[key] is not None:
		# 	# 	issaved = save_file(request.FILES[key], audio_form.cleaned_data, audio, key)
		# 	# 	if issaved:
		# 	messages.success(request,'Artist saved')
		# 	return HttpResponseRedirect(reverse('juno.views.newartist'))
	 	messages.success(request, 'Artist not saved')
	else:
		#AddArtistPhotoForm = inlineformset_factory(Artist, Photo)
		newartist = Artist()
		newphoto = Photo()
		artist_form = AddArtistForm(instance=newartist) #AddArtistPhotoForm(instance=artist)
		photo_form = AddPhotoForm(instance=newphoto)
		
	return render_to_response('juno/newartistphoto.html', {'artist_form': artist_form, 'photo_form': photo_form, }, RequestContext(request))
	


def newartistrecord(request):
	"""docstring for add_event"""
	from juno.forms import AddArtistForm
	from gelder.views import save_file
	key = 'artist'

	if request.method == 'POST':
		artist_form = AddArtistForm(request.POST)
		#raise Exception(request.POST)
		
		recordkey = request.POST['recordtype']
		recordkey = recordkey.lower()
		#raise Exception([recordkey, ])
		if recordkey == 'photo':
			record_form = AddPhotoForm(request.POST, request.FILES)
		elif recordkey == 'audio':
			record_form = AddAudioForm(request.POST, request.FILES)
		else:
			record_form = AddVideoForm(request.POST, request.FILES)
		
		#raise Exception([request.FILES, record_form])
		if artist_form.is_valid() and record_form.is_valid():
			newartist = artist_form.save(commit=True)
			newrecord = record_form.save(commit=False)
			newrecord.caption = newartist.name + " record "
			newrecord.content_object = newartist
			#raise Exception([newphoto.basename, newphoto.photo.name, newphoto.photo.path, newphoto.photo,])
			
			if record_form.cleaned_data[recordkey] is not None:
				issaved = save_file(request.FILES[recordkey], record_form.cleaned_data, newrecord, recordkey)
				if not issaved:
					messages.success(request, 'Related record not saved')
					return HttpResponseRedirect(reverse('juno.views.newartistrecord'))

			newrecord.save()
			messages.success(request,'Artist saved')
			return HttpResponseRedirect(reverse('juno.views.newartistrecord'))
			
	 	messages.success(request, 'Artist not saved')
		return HttpResponseRedirect(reverse('juno.views.newartistrecord'))
	
	else:
		newartist = Artist()
		newphoto = Photo()
		newaudio = Audio()
		newvideo = Video()
		artist_form = AddArtistForm(instance=newartist) 
		photo_form = AddPhotoForm(instance=newphoto, exclude_list=['caption'])
		audio_form = AddAudioForm(instance=newaudio, exclude_list=['caption'])
		video_form = AddVideoForm(instance=newvideo, exclude_list=['caption'])

	return render_to_response('juno/newartistrecord.html', 
						{'artist_form': artist_form, 'photo_form': photo_form,  'audio_form': audio_form,  'video_form': video_form,},
									RequestContext(request))



