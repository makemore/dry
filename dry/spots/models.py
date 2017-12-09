from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.functional import cached_property
from modelcluster.fields import ParentalKey
from django.utils.translation import ugettext as _
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtailgeowidget.edit_handlers import GeoPanel
from wagtailgeowidget.helpers import geosgeometry_str_to_struct



class SpotIndexPage(Page):
	subpage_types = ['spots.SpotPage']

	def children(self):
		return self.get_children().specific().live()

	def get_context(self, request):
		context = super(SpotIndexPage, self).get_context(request)
		context['posts'] = SpotPage.objects.descendant_of(
			self).live().order_by(
			'-date_published')
		return context

class SpotPage(Page):
	date_published = models.DateField(
		"Date article published", blank=True, null=True
	)
	image = models.ForeignKey(
		'wagtailimages.Image',
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='+'
	)
	body = RichTextField()
	address = models.CharField(max_length=250, blank=True, null=True)
	location = models.CharField(max_length=250, blank=True, null=True)

	content_panels = Page.content_panels + [
		FieldPanel('date_published'),
		ImageChooserPanel('image'),
		FieldPanel('body', classname="full"),
		MultiFieldPanel([
			FieldPanel('address'),
			GeoPanel('location', address_field='address'),
		], _('Geo details')),
	]

	parent_page_types = ['spots.SpotIndexPage']
	#subpage_types = ['dryers.DryerPage']

	@cached_property
	def point(self):
		return geosgeometry_str_to_struct(self.location)

	@property
	def lat(self):
		return self.point['y']

	@property
	def lng(self):
		return self.point['x']
