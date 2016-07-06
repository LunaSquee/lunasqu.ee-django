import re
from .models import Topic

class PageViewsMiddleware:
	def process_request(self, request, *args, **kwargs):
		if request.path_info.startswith('/forum/topic/'):
			match = re.search(r'/forum/topic/(\d+)', request.path_info)
			tpcid = match.group(1)
			if tpcid:
				topic = Topic.objects.get(pk=tpcid)
				if topic:
					topic.views += 1
					topic.save()
