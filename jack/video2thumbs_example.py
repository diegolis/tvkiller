# -*- coding: utf8 -*-
import re
import os
import sys
import MySQLdb
import traceback

from simpsons.utils.utils import duration_in_seconds as video_lenght
from simpsons.utils import local_settings


def check_video_thumbs(video, storage, old_storage):
    if video['channel_name'] == 'unknown':
        quantum_storage = storage + video['channel_name'] + '/' + video['dvr'] + '/'\
                      + video['camera'] + '/' + video['date']\
                      + '/' + video['time'] + '/'
        quantum_old_storage = old_storage + video['channel_name'] + '/' + video['dvr'] + '/'\
                      + video['camera'] + '/' + video['date']\
                      + '/' + video['time'] + '/'
    else:
        quantum_storage = storage + video['channel_name'] + '/'\
                          + video['camera'] + '/' + video['date']\
                          + '/' + video['time'] + '/'

        quantum_old_storage = old_storage + video['channel_name'] + '/'\
                          + video['camera'] + '/' + video['date']\
                          + '/' + video['time'] + '/'

    video_last_second = video_lenght(video['fpath'])
    last_thumbnail = str(video_last_second - 2) + '.jpg'
    fcheck = os.path.join(quantum_storage,last_thumbnail)
    fcheck_old = os.path.join(quantum_old_storage,last_thumbnail)

    if os.path.isfile(fcheck) or os.path.isfile(fcheck_old):
        return True
    return False


def mark_video_thumbs(video):
    pass


def main(source, storage, old_storage, date_start=None, date_stop=None, ffmpeg_bin=None):
    """
    ToDo:
    ACTUALIZAR ESTA DESCRIPCIÓN.
    
    
    Esta función se encarga de tomar todos los videos de SOURCE,
    revisar si no ha sido procesado previamente y en caso de que no, generar
    thumb cada segundo.

    Los thumbs serán depositados en:
    STORAGE/channel_name/camera/date/time/

    Los thumbnails tienen el formato xxx.jpg donde x = 0,...,9
    """

    db = MySQLdb.connect(host="192.168.1.206", user="root", passwd="qwertyui", db="InfoadWeb")
    cur = db.cursor()

    for folder in source:
        dirty_files = os.listdir(folder)
        files = []

        # pre-processing to obtain metadata of each file
        for f in dirty_files:
            fpath = os.path.join(folder,f)

            # elude folders and temp files
            if not os.path.isfile(fpath) or "temp" in f:
                continue

            # dict repr of a video file of 10 minutes.
            video = {'filename': f[:-4],
                     'fpath': fpath,
                     'dvr': '',
                     'camera': '',
                     'date': '',
                     'time': '',
                     'channel_name': '',
                    }

            try:
                # Obtain file data
                searchObj = re.search(r'(.*)_(.*)_(.*)_(.*)', video['filename'], re.M|re.I)
                video['dvr'] = searchObj.group(1)
                video['camera'] = searchObj.group(2)
                video['date'] = searchObj.group(3)
                video['time'] = searchObj.group(4)
            except:
                print "Error: not match filename with re"
                continue

            files.append(video)

        # sorting files by date
        sorted(files, key= lambda f: f['date'])

        # filtering by start and stop date
        if date_start:
            files = filter(lambda f: date_start < f['date'], files)

        if date_stop:
            files = filter(lambda f: f['date'] < date_stop, files)


        for video in files:
            query = "select ident_medio from dvr_ident where ident_dvr = '%s' and ident_channel = '%s'" % (video['dvr'], video['camera'])
            cur.execute(query)
            try:
                video['channel_name'] = cur.fetchall()[0][0]
            except:
                video['channel_name'] = 'unknown'

            if video['channel_name'] == 'unknown':
                quantum_storage = storage + video['channel_name'] + '/' + video['dvr'] + '/'\
                              + video['camera'] + '/' + video['date']\
                              + '/' + video['time'] + '/'
            else:
                quantum_storage = storage + video['channel_name'] + '/'\
                                  + video['camera'] + '/' + video['date']\
                                  + '/' + video['time'] + '/'

            try:
                os.makedirs(quantum_storage)
            except:
                pass    # probably folders exists.

            # Check if the video file was previously thumbnailed.
            if check_video_thumbs(video, storage, old_storage):
                continue

            cmd = "%s -i %s -f image2 -vf fps=fps=1 %s"

            cmd = cmd % (ffmpeg_bin, video['fpath'], quantum_storage + '%03d.jpg')
            os.system(cmd)


if __name__=="__main__":

    try:
        ffmpeg = local_settings.FFMPEG
    except:
        ffmpeg = 'ffmpeg' #try ffmpeg_bin installed

    try:
        date_start = local_settings.DATE_START
    except:
        date_start = None

    try:
        date_stop = local_settings.DATE_STOP
    except:
        date_stop = None


    try:
        main(local_settings.SOURCE, 
            local_settings.STORAGE,
            local_settings.OLD_STORAGE, 
            date_start, 
            date_stop,
            ffmpeg)
    except KeyboardInterrupt:
        print "Shutdown requested...exiting."
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)
