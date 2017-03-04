# import sys
# import os
# import re
# import hotshot, hotshot.stats
# import tempfile
# import StringIO
# 
# from django.conf import settings


#http://blog.isotoma.com/2009/12/getting-the-name-of-the-current-view-in-a-django-template/comment-page-1/#comment-884
# also see : http://docs.djangoproject.com/en/dev/topics/http/middleware/
class ViewNameMiddleware(object):
	"""docstring for ViewNameMiddleware"""
	def process_view(self, request, view_func, view_args, view_kwargs):
		request.view_name = ".".join((view_func.__module__, view_func.__name__))
	

# http://villaroad.com/2010/07/monitor-your-django-methods/
# words_re = re.compile(r'\s+')
# group_prefix_re = [
#     re.compile( "^.*/django/[^/]+" ),
#     re.compile( "^(.*)/[^/]+$" ),
#     re.compile( ".*" ),
# ]

# class ProfileMiddleware(object):
#     def process_request(self, request):
#         if (settings.DEBUG or request.user.is_superuser) and 'lookie' in request.GET:
#             self.tmpfile = tempfile.mktemp()
#             self.prof = hotshot.Profile(self.tmpfile)
# 
#     def process_view(self, request, callback, callback_args, callback_kwargs):
#         if (settings.DEBUG or request.user.is_superuser) and 'lookie' in request.GET:
#             return self.prof.runcall(callback, request, *callback_args, **callback_kwargs)
# 
#     def get_group(self, file):
#         for g in group_prefix_re:
#             name = g.findall( file )
#             if name:
#                 return name[0]
# 
#     def get_summary(self, results_dict, sum):
#         list = [ (item[1], item[0]) for item in results_dict.items() ]
#         list.sort( reverse = True )
#         list = list[:40]
# 
#         res = "      tottime\n"
#         for item in list:
#             res += "%4.1f%% %7.3f %s\n" % ( 100*item[0]/sum if sum else 0, item[0], item[1] )
# 
#         return res
# 
#     def summary_for_files(self, stats_str):
#         stats_str = stats_str.split("\n")[5:]
# 
#         mystats = {}
#         mygroups = {}
# 
#         sum = 0
# 
#         for s in stats_str:
#             fields = words_re.split(s);
#             if len(fields) == 7:
#                 time = float(fields[2])
#                 sum += time
#                 file = fields[6].split(":")[0]
# 
#                 if not file in mystats:
#                     mystats[file] = 0
#                 mystats[file] += time
# 
#                 group = self.get_group(file)
#                 if not group in mygroups:
#                     mygroups[ group ] = 0
#                 mygroups[ group ] += time
# 
#         return "&lt;pre&gt;" + \
#                " ---- By file ----\n\n" + self.get_summary(mystats,sum) + "\n" + \
#                " ---- By group ---\n\n" + self.get_summary(mygroups,sum) + \
#                "&lt;/pre&gt;"
# 
#     def process_response(self, request, response):
#         if (settings.DEBUG or request.user.is_superuser) and 'lookie' in request.GET:
#             self.prof.close()
# 
#             out = StringIO.StringIO()
#             old_stdout = sys.stdout
#             sys.stdout = out
# 
#             stats = hotshot.stats.load(self.tmpfile)
#             stats.sort_stats('time', 'calls')
#             stats.print_stats()
# 
#             sys.stdout = old_stdout
#             stats_str = out.getvalue()
# 
#             if response and response.content and stats_str:
#                 response.content = "&lt;pre&gt;" + stats_str + "&lt;/pre&gt;"
# 
#             response.content = "\n".join(response.content.split("\n")[:40])
# 
#             response.content += self.summary_for_files(stats_str)
# 
#             os.unlink(self.tmpfile)
