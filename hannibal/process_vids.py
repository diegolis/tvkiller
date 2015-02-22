# -*- coding: utf8 -*-

from __future__ import print_function

from inotify import watcher
import inotify
import sys
import traceback
import subprocess32

import local_settings

def main(source, storage, ffmpeg_bin=None):

    w = watcher.AutoWatcher()

    try:
        w.add_all(source, inotify.IN_CLOSE_WRITE)
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
            subprocess32.call(["python", "manage.py", "gen_thumb", evt.fullpath, storage, ffmpeg_bin])

if __name__=="__main__":

    try:
        ffmpeg = local_settings.FFMPEG
    except:
        ffmpeg = 'ffmpeg' #try ffmpeg_bin installed

    try:
        main(local_settings.SOURCE, 
            local_settings.STORAGE,
            ffmpeg)
    except KeyboardInterrupt:
        print("Shutdown requested...exiting.")
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)
