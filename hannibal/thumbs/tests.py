from thumbs.models import Clip, Channel
from django.test import TestCase
from datetime import datetime
import os.path
import pytz

# Create your tests here.

class ClipTest(TestCase):

    fixtures = ['origin.json']

    def setUp(self):
        self.channel = Channel.objects.all()[0]

    def test_generar_un_origin(self):

        desde = datetime(2015, 2, 21, 22, 00, 10, tzinfo=pytz.UTC)
        hasta = datetime(2015, 2, 21, 22, 00, 20, tzinfo=pytz.UTC)
        clip = Clip.create_from_channel(self.channel, desde, hasta)
        self.assertTrue(abs(clip.duration - 10) < 0.5)
        self.assertTrue(os.path.exists(clip.filename.path))

    def test_generar_doble_origin(self):

        desde = datetime(2015, 2, 21, 22, 12, 59, tzinfo=pytz.UTC)
        hasta = datetime(2015, 2, 21, 22, 13, 05, tzinfo=pytz.UTC)
        clip = Clip.create_from_channel(self.channel, desde, hasta)
        self.assertTrue(os.path.exists(clip.filename.path))
        self.assertTrue(abs(clip.duration - 6) < 0.5)

