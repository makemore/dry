from django.contrib import admin
from .models import SpotAV

# Register your models here.

def render_video(modeladmin, request, queryset):
    for video in queryset:
        video.render()


render_video.short_description = "Render Video"


def add_render_to_queue(modeladmin, request, queryset):
    for video in queryset:
        video.job_added_to_queue_once = False
        video.save() z
        video.add_render_to_queue()


add_render_to_queue.short_description = "add_render_to_queue"


def add_to_new_spot_page(modeladmin, request, queryset):
    for video in queryset:
        video.add_to_new_spot_page()


add_to_new_spot_page.short_description = "add_to_new_spot_page"


class SpotAVAdmin(admin.ModelAdmin):
    # list_display = ['title', 'status']
    # ordering = ['title']
    actions = [render_video, add_render_to_queue, add_to_new_spot_page]


admin.site.register(SpotAV, SpotAVAdmin)
