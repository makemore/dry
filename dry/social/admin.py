from django.contrib import admin
from .models import SpotAV


# Register your models here.

def render_video(modeladmin, request, queryset):
    for video in queryset:
        video.render()


render_video.short_description = "Render Video"


def add_to_new_spot_page(modeladmin, request, queryset):
    for video in queryset:
        video.add_to_new_spot_page()


add_to_new_spot_page.short_description = "add_to_new_spot_page"


class SpotAVAdmin(admin.ModelAdmin):
    # list_display = ['title', 'status']
    # ordering = ['title']
    actions = [render_video, add_to_new_spot_page]


admin.site.register(SpotAV, SpotAVAdmin)
# admin.site.register(SpotAV)
