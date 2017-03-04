from django import forms
from django.forms import ModelForm
from django.forms import extras

from models import Artist
from gelder.models import Record, Audio, Video, Photo

class AddArtistForm(ModelForm):
	"""docstring for AddPhotoForm"""
	recordtype = forms.CharField(widget=forms.Select(choices=Record.RECORD_TYPES),  
			max_length=32, help_text="Select the type of media to link to the artist")
	class Meta:
		"""docstring for Meta"""
		model = Artist
		#exclude = ['record']
		
	

