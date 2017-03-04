from sorethumb.filters.defaultfilters import *
from sorethumb.filters.drawfilters import *
from sorethumb.djangothumbnail import DjangoThumbnail

class RoundedCornersBackground(DjangoThumbnail):
    name = 'small_profile_image'
    format = 'png'
    filters = [ThumbnailFilter(120, 100),
               RoundedCornerFilter(10, border='#333'),
               ResizeCanvasFilter(130, 110, '#fff'),
               OpaqueFilter('#fff')]

class SmallThumb(DjangoThumbnail):
	format = 'png'    
	filters = [ThumbnailFilter(120, 100)]

class MediumThumb(DjangoThumbnail):
	format = 'png'    
	filters = [ThumbnailFilter(180, 150)]

class LargeThumb(DjangoThumbnail): 
    format = 'png'   
    filters = [ThumbnailFilter(360, 300)]

class RoundedCorners5(DjangoThumbnail):    
    format = 'png'
    filters = [ThumbnailFilter(120, 100),
               RoundedCornerFilter(5)]

class OriginalImage(DjangoThumbnail):    
    format = 'png'
    filters = [RoundedCornerFilter(2)]

class EventDisplay(DjangoThumbnail):
	"""docstring for EventDisplay"""
	format = 'png'
	filters = [FixedHeightFilter(560), ] #FixedWidthFilter(640),#ResizeCanvasFilter(640,480,background_color='#303030'),]
		