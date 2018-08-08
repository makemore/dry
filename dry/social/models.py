from django.db import models
from dry.models import BaseModel
# Create your models here.

class SpotAV(BaseModel):
    image = models.ImageField(upload_to="spot-av")
    audio = models.FileField(upload_to="spot-av")
    video = models.FileField(upload_to="spot-av")