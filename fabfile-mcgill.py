from __future__ import with_statement
from fabric.api import *
from fabric.utils import warn


env.user='root'

#env.hosts=["sweps.ece.mcgill.ca","storm.ece.mcgill.ca"]
#env.hosts=["jupiter.ece.mcgill.ca"]
env.roledefs={
	'web':['sweps.ece.mcgill.ca'],
	'compute': ['jupiter.ece.mcgill.ca','tri.ece.mcgill.ca','quartet.ece.mcgill.ca','chamonix.ece.mcgil.ca','c01.ece.mcgill.ca','c03.ece.mcgill.ca','c04.ece.mcgill.ca','driver.ece.mcgill.ca','duet.ece.mcgill.ca','jupiter.ece.mcgill.ca','lisa.mcgill.ca','monster.ece.mcgill.ca','c017.ece.mcgill.ca','quartet.ece.mcgill.ca','ricky.ece.mcgill.ca'],
	'storm': ['storm.ece.mcgill.ca'],
	'tabots':['mm-tabot.ece.mcgill.ca','tabot.ece.mcgill.ca'],
	'meyer':['amonhen.ece.mcgill.ca','emynmuil.ece.mcgill.ca'],
	'test':['ce-tabot.ece.mcgill.ca'],
	'aries':['aries.ece.mcgill.ca'],
	'tux':['132.206.19.82'],
	'smbtest':['c017.ece.mcgill.ca'],
}
#env.parallel=True

#print("Executing on %s as %s" % (env.hosts, env.user))

#ERROR HANDLING
#
#Skip offline hosts
env.skip_bad_hosts=True
#Timout for connection chesk
env.timeout=2
#while executing to give only a warning instead aborting
env.warn_only=True
#wrning example for certain command only
#def cmd(cmd):
#    with settings(warn_only=True):
#	run(cmd)
#more structured 
#@serial
#def cmd(cmd):
#    with settings(warn_only=True):
#        if run(cmd).failed:
#            sudo(cmd)


#COMMAND
def myservers():
	env.hosts=["sweps.ece.mcgill.ca","ricky.ece.mcgill.ca"]

def host_type():
	run ('uname -s')

def uptime():
	run ('uptime')

def version():
	run ('cat /etc/issue')

def lcmd():
	local('echo fabtest >> test.log')

def send(localpath,remotepath):
	put(localpath,remotepath,use_sudo=True)

def get(remotepath,localpath):
	get(remotepath,localpath+"."+env.host)

#def web2():
#	env.hosts=["sweps.ece.mcgill.ca"]
#	env.skip_bad_hosts=True

def sslcheck():
	run('sudo openssl version -a')

def sslupdate():
	run('yum -y update openssl')

def who():
	run('who')

def secure():
	run('cat /var/log/secure')

def screen_install():
	run('yum -y install screen')

#SAMBA 

def sambaservices():
	run('netstat -tulpn | egrep "samba|smbd|nmbd|winbind"')

#Provide copmatibility for older gcc versions back to gcc 3.4
def gcc_compat():
	packages="compat-gcc-34-3.4.6-19.el6.x86_64 compat-gcc-34-c++-3.4.6-19.el6.x86_64 compat-gcc-34-g77-3.4.6-19.el6.x86_64"
	run('yum -y install %s' %packages)

#VAS
def vasjoin():
	run('/opt/quest/bin/vastool - u bratislav.mladjic@campus.mcgill.ca join -f -w campus.mcgill.ca')

def vasflush():
	run('vastool flush')

def vasrestart():
	run('service vasd restart')

def usersallow():
	run('cat /etc/opt/quest/vas/users.allow')
#TA system
def tasetup():
	run('apt-get update')
	run('apt-get -y install apache2')
	run('apt-get -y install libapache2-mod-auth-mysql php5-mysql')
	run('apt-get -y install php5 libapache2-mod-php5 php5-mcrypt')
#	run('apt-get install phpmyadmin')
	run('apt-get install exim4')


def mysqlinstall():
	packages="mysql-server libapache2-mod-auth-mysql php5-mysql"
	run('apt-get -y install %s' % packages)
	run('mysql_secure_installation')

def phpmyadmininstall():
	run('apt-get install phpmyadmin')

#Additional php files defined in the document "Setting up a TA System"
def phpadd():
	packages="php5-mysql php5-curl php5-gd php5-idn php-pear php5-imagick php5-imap php5-mcrypt php5-memcache php5-mhash php5-ming php5-ps php5-pspell php5-recode php5-snmp php5-sqlite php5-tidy php5-xmlrpc php5-xsl php-mcrypt"
	run('apt-get -y install %s' % packages)

def apt_get(*packages):
	run('apt-get -y --no-upgrade install %s' % ' '.join(packages), shell=False)
	
#Copies files from mm-tabot.ece.mcgill.ca:/var/www/ to destination 
def cp_www():
	run("scp root@mm-tabot.ece.mcgill.ca:/var/www/ /var/www/")

#Copies folder from mm-tabot.ece.mcgill.ca:/opt/scripts to /opt/
def cp_scripts():
	run('scp -r root@mm-tabot.ece.mcgill.ca:/opt/scripts /opt/')

def mysql():
	with settings(hide('warnings', 'stderr'), warn_only=True):
		result=('dpkg-query --show mysql-server')
	if result.failed is False:
		warn('MySQL is already installed')
	return
#	run('echo "mysql-server5.0 mysql-server/root_password password' '%s" | debconf-set-selections' %mysql_password)
#	run('echo "mysql-server5.0 mysql-server/root_password_again password' '%s" | debconf-set-selections' %mysql_password)

#TASKS
#@task
def command(cmd):
	run(cmd)

@roles('web')
def lsvar():
	run ('ls -al /var/www/')

@roles('compute')
def cversion():
	run ('cat /etc/issue')

#COMMENT: When role active, it will override -R for role in command fab -R <role
#roles('compute')
#ef who():
#       run('who')

#roles('compute')
#ef version_compute():
#run('cat /etc/issue')

@roles('aries')
def ECE():
	run('cat /var/named/chroot/var/named/ECE.McGill.CA')

#@aries
#def clsexport():
#	with settings(user="bratislav.mladjic",host_string="storm.ece.mcgill.ca")
#	run('ls -al /export/')

#@parallel
#def pcmd(cmd):
#	run(cmd)
