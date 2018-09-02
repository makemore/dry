from django.contrib import admin
from .models import SpotAV

# Register your models here.

def render_video(modeladmin, request, queryset):
    for video in queryset:
        video.render()
render_video.short_description = "Render Video"

class SpotAVAdmin(admin.ModelAdmin):
    #list_display = ['title', 'status']
    #ordering = ['title']
    actions = [render_video]

admin.site.register(SpotAV, SpotAVAdmin)
#admin.site.register(SpotAV)