from django.db import models
from django.conf import settings
import os

# Create your models here.
class Channel(models.Model):
    name = models.CharField(max_length=200, unique=True)
    device_name = models.CharField(max_length=200, default="")
    device_slot = models.CharField(max_length=200, default="")

    def save(self, *args, **kwargs):
        """ Create a directory for the thumbnails. """
        super(Channel, self).save(*args, **kwargs)
        try:
            os.mkdir(self.base_dir())
        except OSError:
            pass

    def __str__(self):
        return self.name

    def base_dir(self):
        return os.path.join(settings.THUMB_DIR, str(self.id))


class Origin(models.Model):
    channel = models.ForeignKey(Channel)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    filename = models.CharField(max_length=200)

    def duration(self):
        """ Returns deltatime """
        return self.end_time - self.start_time
