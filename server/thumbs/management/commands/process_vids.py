# -*- coding: utf8 -*-

from __future__ import print_function

from django.core.management.base import BaseCommand, CommandError
from inotify import watcher
import inotify
import sys
import traceback
import subprocess32

from django.conf import settings

def main(source, ffmpeg_bin=None):

    w = watcher.AutoWatcher()

    try:
        w.add_all(source, inotify.IN_CREATE)
    except OSError as err:
        print('%s: %s' % (err.filename, err.strerror), file=sys.stderr)

    # If we have nothing to watch, don't go into the read loop, or we'll
    # sit there forever.

    if not w.num_watches():
        print("no files to watch", file=sys.stderr)
        sys.exit(1)

    while w.num_watches():
        # The Watcher.read method returns a list of event objects.
        for evt in w.read():
            # The inotify.decode_mask function returns a list of the
            # names of the bits set in an event's mask.  This is very
            # handy for debugging.
            if not ".listing" in evt.fullpath:
                subprocess32.Popen(["/home/infoxel/envs/hannibal/bin/python", "/home/infoxel/tvkiller/server/manage.py", "gen_thumb", evt.fullpath, ffmpeg_bin])


class Command(BaseCommand):

    def handle(self, *args, **options):

        try:
            ffmpeg = settings.FFMPEG
        except:
            ffmpeg = 'ffmpeg' #try ffmpeg_bin installed
    
        try:
            main(settings.SOURCE, 
                ffmpeg)
        except KeyboardInterrupt:
            print("Shutdown requested...exiting.")
        except Exception:
            traceback.print_exc(file=sys.stdout)
        sys.exit(0)
    