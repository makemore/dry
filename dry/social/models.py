from django.db import models
from dry.models import BaseModel
# Create your models here.
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip, \
    ImageSequenceClip
import moviepy.video.fx.all as vfx
from moviepy.editor import concatenate_videoclips
from moviepy.video.fx.all import crop


class SpotAV(BaseModel):
    image = models.ImageField(upload_to="spot-av", blank=True)
    audio = models.FileField(upload_to="spot-av", blank=True)
    video = models.FileField(upload_to="spot-av", blank=True)

    def render(self):
        if self.image is None or self.audio is None:
            raise Exception("no image or audio present")
        audio_clip = AudioFileClip(self.audio.path)

        image_clip = ImageClip(self.image.path)
        image_clip.set_duration(audio_clip.duration)

        logo_clip = ImageSequenceClip("./compositing_assets", fps=30, durations=audio_clip.duration)
        logo_clip.set_position((0.4, 0.7), relative=True)
        # logo_clip =

        final_clip = concatenate_videoclips([logo_clip, logo_clip, logo_clip, logo_clip, logo_clip])

        # logo_clip_2 = logo_clip.fx(vfx.loop, n=5, duration=audio_clip.duration, )

        # logo_clip_2.set_duration(5)
        final_clip.set_position((0.4, 0.7), relative=True)  # .set_duration(5)

        video = CompositeVideoClip([image_clip, final_clip]).set_audio(audio_clip)

        video.duration = audio_clip.duration
        (w, h) = video.size
        video.write_videofile("myHolidays_edited.mp4", fps=30, codec="h264")
        #cropped_clip = crop(video, width=1280, height=720, x_center=w / 2, y_center=h / 2)
        #cropped_clip.write_videofile("myHolidays_edited.mp4", fps=30, codec="h264")

        print(self)
