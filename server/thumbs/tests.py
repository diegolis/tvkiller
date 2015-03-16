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

        desde = datetime(2015, 2, 21, 22, 00, 00, tzinfo=pytz.UTC)
        hasta = datetime(2015, 2, 21, 22, 01, 00, tzinfo=pytz.UTC)
        clip = Clip.create_from_channel(self.channel, desde, hasta)
        self.assertEqual(clip.duration, 60)
        self.assertTrue(os.path.exists(clip.filename.path))

