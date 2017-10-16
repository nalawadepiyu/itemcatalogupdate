<h1> Linux Server Configuration </h1>
<p>
<ul>
<li>Local IP Address: 54.148.219.205</li>
<li>SSH port: 2200</li>
<li>Login with ssh -i grader@54.148.219.205 </li>
<li>Do ssh-keygen get id_rsa.pub key from your local machine and save in /home/grader/.ssh/authorized_keys in Lightsail AWS instance</li>
</ul>
</p>
<br>
<h1>Configuration:</h1>
<h2>Launch Instance: 
<ul>
<li>Amazon Lightsail Instance username: ubnutu</li>
<li> Public IP: 54.148.219.205 </li>
</ul>
<h2>
<ul>
<li>Save id_rsa.pub key in /home/grader/.ssh/authorized_keys </li>
</ul>
<h2>Upgrade Instance packages</h2>
<ul>
<li>Run sudo apt-get update</li>
<li> Run sudo apt-get upgrade </li>
</ul>
<h2>change port 22 to 2200 in /etc/ssh/sshd_config</h2>
<h2>Configure firewall:</h2>
<ul>
<li>sudo ufw status</li>
<li>sudo ufw allow 2200/tcp</li>
<li>sudo ufw allow 80/tcp</li>
<li>sudo ufw allow 123/udp</li>
<li>sudo ufw enable</li>
<li>sudo ufw status</li>
</ul>
<h2>Grader Access:</h2>
<ul>
<li>sudo adduser grader</li>
<li>su - grader </li>
<li> mkdir .ssh </li>
<li> touch authorized_keys </li>
<li> save id_rsa.pub key in /home/grader/.ssh/authorized_keys</li>
<li>chmod 700 .ssh</li>
<li>chmod 644 authorized_keys</li>
<li>vim etc/sudoers.d/grader and type grader ALL=(ALL:ALL) ALL</li>
</ul>
<h2> Configure the local timezone to UTC</h2>
<p>Configure timezone sudo dpkg-reconfigure tzdata </p>
<h2>configure wsgi:</h2>
<ul>
<li>sudo apt-get install git</li>
<li>sudo apt-get install libapache2-mod-wsgi</li>
<li>sudo service apache2 restart</li>
<li>Create FlaskApp directory in /var/www</li>
<li>inside FlaskApp git clone https://github.com/nalawadepiyu/itemcatalogupdate.git</li>
<li>sudo mv ./itemcatalogupdate ./FlaskApp</li>
<li>Replace engine = create_engine('sqlite:///catalogDB.db') by <br>
engine = create_engine('postgresql://catalog:password@localhost/catalog') in database_setup.py, details.py, catalogproject.py</li>
<li>Rename catalogproject.py to __init__.py</li>
<li>edit path for clients_secrets.json in __init__.py: by import os</li>
<li>path = os.path.dirname(__file__)</li>
<li>CLIENT_ID = json.loads(open(path+'/client_secrets.json', 'r').read())['web']['client_id']</li>
<li>sudo apt-get install python-pip</li>
<li>sudo apt-get -qqy install postgresql python-psycopg2</li>
<li>Install sqlalchemy, flask, requests, httplib2</li>
<h2>Configure PostgreSQL:</h2>
<li>sudo apt-get install postgresql</li>
<li>sudo su - postgres</li>
<li>psql</li>
<li>Create DB: postgres=# CREATE DATABASE catalog;</li>
<li>postgres=# CREATE USER catalog</li>
<li>Set password : postgres=# ALTER ROLE catalog WITH PASSWORD 'password';</li>
<li>give access: postgres=# GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog;</li>
<li>\q and type exit to exit from postgres role</li>
<li>sudo python database_setup.py</li>
<li>sudo python details.py</li>
<h2>Create .wsgi file: under /var/www/FlaskApp</h2>
<li>sudo nano flaskapp.wsgi</li>
<li>Add following line in flaskapp.wsgi file</li>
<p>
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FlaskApp/")

from FlaskApp import app as application
application.secret_key = 'Add your secret key'
</p>
<br>
<li>sudo nano /etc/apache2/sites-available/FlaskApp.conf</li>
<p>
<VirtualHost *:80>
	ServerName 54.148.219.205
	ServerAdmin priyankanalawade108@gmail.com
	WSGIScriptAlias / /var/www/FlaskApp/flaskapp.wsgi
	<Directory /var/www/FlaskApp/FlaskApp/>
		Order allow,deny
		Allow from all
	</Directory>
	ErrorLog ${APACHE_LOG_DIR}/error.log
	LogLevel warn
	CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
</p>
<h2>Restart Apache:</h2>
<p>sudo service apache2 restart</p>
</ul>

