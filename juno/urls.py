from django.conf.urls.defaults import * 


urlpatterns = patterns('',
	(r'^view/(?P<name>[-\w]+)/$','juno.views.aindex', {}, 'juno_artist_view'),
	(r'^newartist$','juno.views.newartist', {}, 'juno_newartist'),
	(r'^newartistphoto$','juno.views.newartistphoto', {}, 'juno_newartistphoto'),
	(r'^newartistrecord$','juno.views.newartistrecord', {}, 'juno_newartistrecord'),
	#(r'^newphoto$','gelder.views.newphoto', {}, 'gelder_newphoto'),
	#(r'^newvideo$','gelder.views.newvideo', {}, 'gelder_newvideo'),
	# (r'^youtube/$','gelder.views.event_youtube', {}, 'gelder_events_youtube'),
	# (r'^reset/$','gelder.views.reset_events', {}, 'gelder_reset_events'),
	# (r'^uptos3/$','gelder.views.uploadphototos3', {}, 'gelder_up_photos'),
	# (r'^ajax_now_html/$','gelder.views.event_now_html_ajax', {}, 'gelder_events_now_html_ajax'),
	# (r'^ajax_now/$','gelder.views.event_now_ajax', {}, 'gelder_events_now_ajax'),
	# (r'^ajax_next/$','gelder.views.event_next_ajax', {}, 'gelder_events_next_ajax'),
	# # (r'^ajax_login/$','gelder.views.ajax_user_login', {}, 'gelder_user_login_ajax'),
	# # (r'^ajax_loadnav/$','gelder.views.load_nav_ajax', {}, 'gelder_load_nav_ajax'),
	# (r'^all/$','gelder.views.event_list', {}, 'gelder_events'),
	# (r'^add/$','gelder.views.event_add',{}, 'gelder_event_add'),
	# (r'^edit/(?P<event_slug>[-\w]+)/$','gelder.views.event_edit',{}, 'gelder_event_edit'),
	# (r'^drop/(?P<event_slug>[-\w]+)/$','gelder.views.event_drop',{}, 'gelder_event_drop'),
	# (r'^view/(?P<slug>[-\w]+)/$','gelder.views.event_detail', {}, 'gelder_event_detail'),
	# (r'^aart/(?P<audio_slug>[-\w]+)/$','gelder.views.audioart_add', {}, 'gelder_audioart_add'),

)