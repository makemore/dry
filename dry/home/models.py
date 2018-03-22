from __future__ import absolute_import, unicode_literals

from wagtail.wagtailcore.models import Page, Orderable
from spots.models import SpotIndexPage


class HomePage(Page):
    pass

    # subpage_types = ['dryers.DryerIndexPage']

    @property
    def spot_pages(self):
        pages = SpotIndexPage.objects.all()[0].children()[:5]
        found = False
        index = -1
        while not found:
            index += 1
            if pages[index].image is not None:
                found = True
        return pages[index]
