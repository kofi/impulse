from django import template
# from django.conf.urls.defaults import *
register = template.Library()

@register.inclusion_tag('forms/formerrors.html')
def print_form_errors(f):
	"""docstring for print_form_errors"""
	return {'form': f}