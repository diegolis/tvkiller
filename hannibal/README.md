# install virtualenvwrapper

`pip install virtualenvwrapper`

## make virtualenv available on login shells

`echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/infoxel/.bashrc`
`echo "export WORKON_HOME=/home/infoxel/envs" >> /home/infoxel/.bashrc`
`mkdir $WORKON_HOME`

## make virtualenv for hannibal

`mkvirtualenv hannibal`

# Set up for hannibal django project

## clone this repo
`cd /home/infoxel && git clone https://github.com/diegolis/tvkiller.git`
`cd /home/infoxel/tvkiller/hannibal`

## fullfill requirements
`pip install -r requirements.txt`

## edit local settings

```
cat tvkiller/hannibal/local_settings.py

FFMPEG = '/usr/bin/ffmpeg'
SOURCE = '/var/www/source_videos_tvkiller/'
```

## load initial data

`python manage.py loadddata thumbs/fixtures/hannibal__thumbs__channel.json`


## setup crontab


```
# generate thumbs for new videos
0 * * * * ( flock -n 9 || exit 1; ( /home/infoxel/envs/hannibal/bin/python /home/infoxel/tvkiller/hannibal/process_vids.py )) 9> /home/infoxel/locks/process_vids.lock
```

