from django import template
# from django.conf.urls.defaults import *
register = template.Library()

@register.tag(name="html_link")
def do_html_link(parser, token):
	"""docstring for do_html_link"""
	# try:
	# 	tag_name, link_text, link_url = token.split_contents() #,  link_attrs
	# except ValueError:
	bits = token.split_contents()
	if len(bits) < 3:
		raise template.TemplateSyntaxError, "%r tag at least three params" % token.contents.split()[0]
	link_text= bits[1]
	link_url= bits[2]
	kwargs= {}
	if len(bits)>3:
		link_attrs = bits[3:]
	 	for l in link_attrs:
			k, a = l[1:-1].split(":-")
			# k & a come in as unicode strings u'a' etc so need to recast as a string tupe or we get errors
			kwargs[str(k)] = str(a)		
	return HtmlLinkNode(link_text, link_url, **kwargs)
	
class HtmlLinkNode(template.Node):
	"""docstring for HtmlLinkNode
	Renders a loaded Html Link called from do_html_link
	Example:
	
	{% html_link link_text link_url "class:-classname1 classname1" "target:-target_value" %}
	
	link_url can either a string path or a url value processed with the 'url' template tag
	"""
	def __init__(self, link_text, link_url, **kwargs): #, link_args = None, link_attrs=None
		"""docstring for __init_"""
		self.link_text = link_text
		if self.link_text[0] == self.link_text[-1] and self.link_text[0] in ('"', "'"):
			self.link_text = self.link_text[1:-1]
		if not (link_url[0] == link_url[-1] and link_url[0] in ('"', "'")):
			self.link_url = template.Variable(link_url)
			self.isvariable = True
		else:
			self.link_url = link_url[1:-1]
			self.isvariable = False
			
		self.link_attrs=kwargs

	def render(self,context):
		"""docstring for render"""
		link_attrs = ''
		if self.link_attrs is not None:
			for lattr, attrval in self.link_attrs.items():
				link_attrs = '%s %s="%s" ' % (link_attrs, lattr, attrval)
		if not self.isvariable:		
			return """ <a href="%s" %s>%s</a> """ % (self.link_url, link_attrs, self.link_text) 
		else :
			try:
				linkurl = self.link_url.resolve(context)
				return """<a href="%s" %s>%s</a>""" % (linkurl, link_attrs, self.link_text)
			except template.VariableDoesNotExist:
				return ''
