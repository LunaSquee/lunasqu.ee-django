from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify

class Post(models.Model):
	title = models.CharField(max_length=140)
	slug = models.SlugField()
	body = models.TextField()
	created = models.DateTimeField(auto_now=True)
	updated = models.DateTimeField()

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		
		if not self.id:
			self.created = timezone.now()
		self.updated = timezone.now()

		super(Post, self).save(*args, **kwargs)

	def __str__(self):
		return self.title
