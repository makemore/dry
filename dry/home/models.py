from __future__ import absolute_import, unicode_literals

from wagtail.wagtailcore.models import Page, Orderable
from spots.models import SpotIndexPage

class HomePage(Page):
	pass
	#subpage_types = ['dryers.DryerIndexPage']

	@property
	def spot_pages(self):
		pages = SpotIndexPage.objects.all()[0].children()[:1]
		return pages

