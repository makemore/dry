from __future__ import absolute_import, unicode_literals

from wagtail.wagtailcore.models import Page, Orderable
from spots.models import SpotIndexPage, SpotPage


class HomePage(Page):
    pass

    # subpage_types = ['dryers.DryerIndexPage']

    @property
    def spot_pages(self):
        pages = SpotPage.objects.order_by("-facebook_created")[:5]
        found = False
        index = -1
        while not found:
            index += 1
            if pages[index].image is not None:
                found = True
        return pages[index]
