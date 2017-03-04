# Django settings for impulse project.
import djcelery
djcelery.setup_loader()

DEBUG = True
TEMPLATE_DEBUG = DEBUG

import os
SITE_ROOT = os.path.realpath(os.getcwd()) 
PROJECT_NAME = os.path.basename(SITE_ROOT)
ALL_MEDIA_ROOT = os.path.join(os.path.dirname(SITE_ROOT), 'files')


ADMINS = (
     ('****', '***.web@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '*#*#*##*#*#',                      # Or path to database file if using sqlite3.
        'USER': '*#*#*#*#',                      # Not used with sqlite3.  #u:root p:#Koomintah06$
        'PASSWORD': '**#**#*#',                  # Not used with sqlite3. 
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# for the debug toolbar
INTERNAL_IPS = ('127.0.0.1',)

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(ALL_MEDIA_ROOT,PROJECT_NAME) 

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL_BASE = 'site_media'
MEDIA_URL = os.path.join('http://localhost:8000',MEDIA_URL_BASE,'')
#MEDIA_URL = 'os.path.join(ALL_MEDIA_ROOT,PROJECT_NAME)'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_DOC_ROOT = MEDIA_ROOT 	#''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/site_media/media/' #'/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '-8yAdsja072cwr#@&(#tn%0i$tp7@n61)v!nmToInF1n1t1AndB3y0Ndqz^n%(is$2%6)c^5t0y#g-(wzm2#'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
	'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'impulse.middleware.ViewNameMiddleware',
)

ROOT_URLCONF = 'impulse.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT,'templates'),     #'/Users/moloo/devel/pythondev/django/wall/templates/',
    os.path.join(os.path.dirname(SITE_ROOT),'israel/templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'django.contrib.flatpages',
    'debug_toolbar',
    'israel',
    'gelder',
    'juno',
    'djcelery',
    'ghettoq',
    'djkombu',
)


# settings for File
FILE_UPLOAD_MAX_MEMORY_SIZE = 0
FILE_UPLOAD_PERMISSIONS = 0777

# where to upload files on the local server
GELDER_LOCAL_PHOTO_UPLOADTO = 'gelder/photo/'
GELDER_LOCAL_VIDEO_UPLOADTO = 'gelder/video/'
GELDER_LOCAL_AUDIO_UPLOADTO = 'gelder/audio/'

# settings for photo thumbs and display generation
GELDER_PHOTO_THUMB_TAG = 'thumb_'
GELDER_PHOTO_DISPLAY_TAG = 'display_'

# use either AWS or localhost host to serve Photo or Audio assets
GELDER_MEDIA_FILESERVER = 'aws'   # options 'localhost' or 'aws

# Keys for Amazon AWS + S3
GELDER_AWS_ACCESS_KEY_ID = '#*#*#*#*#*#*#**####'
GELDER_AWS_SECRET_ACCESS_KEY = '#*#*#*#*#*#****#**##*#**##'

# S3 BUCKETS
GELDER_S3_PHOTO_BUCKET = 'impulsegelderphotos'
GELDER_S3_PHOTO_THUMB_BUCKET = 'impulsegelderphotosthumb'
GELDER_S3_PHOTO_DISPLAY_BUCKET = 'impulsegelderphotosdisplay'
GELDER_S3_AUDIO_BUCKET = 'impulsegelderaudio'
GELDER_S3_AUDIOART_BUCKET = 'impulsegelderaudioart'
GELDER_S3_VIDEO_BUCKET = 'impulsegeldervideo'

#DEFAULT_FROM_EMAIL = 'outbound@ontheadwall.com'

DEBUG_TOOLBAR_CONFIG = { 'INTERCEPT_REDIRECTS': False }
SORETHUMB_OUTPUT_PATH = os.path.join(MEDIA_ROOT,'thumbs') #'/Users/moloo/devel/pythondev/django/files/wall/thumbs/'
SORETHUMB_URL_ROOT= os.path.join('/', MEDIA_URL_BASE, 'thumbs', '') #'/site_media/thumbs/'
SORETHUMB_IMAGE_ROOT= MEDIA_ROOT
SORETHUMB_DEFAULT_IMAGE= os.path.join(MEDIA_ROOT,'default.jpg') #'/Users/moloo/devel/pythondev/django/files/wall/default.jpg'

# CELERY + ghettoq config
# more config options : http://celeryq.org/docs/configuration.html
CELERYD_CONCURRENCY = 2
BROKER_HOST = 'localhost'
BROKER_PORT = 5672
BROKER_USER = '#^#^$'
BROKER_PASSWORD = '#&#&#&#'
BROKER_VHOST = '/'
BROKER_BACKEND = 'django'  #'ghettoq.taproot.Database' #, 'django' #
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

BOOTSTRAP_FOLDER = os.path.join(MEDIA_ROOT,'bootstrap') 


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler'
#         }
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     }
# }
