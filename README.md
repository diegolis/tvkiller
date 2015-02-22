# tvkiller


instalar celery
///////////////


pip install celery
pip install redis

sudo apt-get install redis-server

para correr los workers, dentro del virtualenv

$ celery -A hannibal worker -l info