#from fabric.api import cd, env, prefix, run, task
from fabric.api import *

env.hosts = ['xbian@192.168.1.101']

@task
def backup():
    run('scp 192.168.1.104:/xbmc-backup/backup* /home/bratislav/Desktop/PYTHON/')

@task
def memory_usage():
    run('free -m')

@task
def deploy():
    with cd('/var/www/project-env/project'):
        with prefix('. ../bin/activate'):
            run('git pull')
            run('touch app.wsgi')
@task
def hello():
	print("Hello python world !")

@task
def host_type():
    run ('uname -s')

@task
def hostname_check():
    run ("hostname")

@task
def reboot():
    run ("sudo reboot")


def mysqlinstall():
	packages="mysql-server php5-mysql"
	run('apt-get -y install %s' % packages)
	run('sudo mysql_install_db')
	run('sudo /usr/bin/mysql_secure_installation')

def nginxinstall():
	run('sudo apt-get install nginx')
	run('sudo service nginx start')




