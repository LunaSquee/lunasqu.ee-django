from django import template
from forum.settings import DJANGO_SIMPLE_FORUM_REPLIES_PER_PAGE as repliesperpage

register = template.Library()

def postnumber(value, arg):
	return value + (repliesperpage * (arg - 1))

register.filter('postnumber', postnumber)
