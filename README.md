# Coffeenator
This is a simple interface for controlling coffee machines via web.  
I created it as part of a school project with a Raspberry Pi system.  
Could be useful for others, who want to control their coffee machines remotely.  

## Requirements
First of all, you need a properly setup Raspberry and a coffee machine with hardware keys.  
You'll need connect the Raspberry with the coffee machine by using a relays-board like [this](http://www.sainsmart.com/16-channel-12v-relay-module-for-pic-arm-avr-dsp-arduino-msp430-ttl-logic.html).  
>**Note:** This requires soldering some wires and in my opinion also a lot of patience.  

If you have any question, feel free to contact me.  

## Dependencies
* **Libraries:**  
This is needed to run coffeenator successfully.
  * python2.7
  * python-dev
  * python-django
  * python-RPI.GPIO
  * python-mysqldb
  * python-gettext
* **Database:**  
Can be any supported database by Django.  
I have used MySQL, which has been a pretty good choice so far.  
* **Webserver:**  
Can be any Webserver with proxy-capabilities (e.g. Apache2 or Nginx).

## Installation
The following information describes the installation on Raspbian.  
Everything can be done easily by using apt-get.  

### Project libraries
```bash
apt-get install python2.7 python-dev python-django python-RPI.GPIO python-mysqldb gettext
```

### MySQL Server
```bash
apt-get install mysql-server
mysql -u root -p -e "DROP DATABASE IF EXISTS coffeenator;
CREATE DATABASE coffeenator; 
GRANT ALL PRIVILEGES ON coffeenator.* TO 'coffeenator'@'%' IDENTIFIED BY 'coffeenator';
FLUSH PRIVILEGES;
```

### Coffeenator
```bash
apt-get install git
git clone https://github.com/blue-ananas/coffeenator.git /opt/coffeenator
chown -R root.root /opt/coffeenator
```

Change default settings  
```bash
cp /opt/coffeenator/webinterface/default_settings.py /opt/coffeenator/webinterface/settings.py
editor /opt/coffeenator/webinterface/settings.py
```

Sync the database  
```bash
/opt/coffeenator/manage.py syncdb
```

You can start the software manually by entering the this commands:  
```bash
/usr/bin/python /opt/coffeenator/manage.py runserver &
service apache2 restart
```

In order to automatically starting coffeenator at boot, enter the following commands into /etc/rc.local before the "exit 0"-line.  
```bash
/usr/bin/python /opt/coffeenator/manage.py runserver & 1>> /var/log/coffeenator.log 2>&1
service nginx reload
exit 0
```

### Nginx
To forward requests to coffeenator (port 8000), you could use Nginx.  
```bash
apt-get install nginx ssl-cert
cp /opt/coffeenator/doc/nginx/coffeenator.conf /etc/nginx/sites-available/coffeenator.conf
ln -s /etc/nginx/sites-enabled/coffeenator.conf  /etc/nginx/sites-available/coffeenator.conf
```

>**Note:** Right now, the software only runs with root-privileges, which can be unsafe.
>Therefore, I suggest you to run it on a private network only.

## License
General Public License, Version 3.0  

>This program is free software: you can redistribute it and/or modify  
>it under the terms of the GNU General Public License as published by  
>the Free Software Foundation, either version 3 of the License, or  
>(at your option) any later version.  
>  
>This program is distributed in the hope that it will be useful,  
>but WITHOUT ANY WARRANTY; without even the implied warranty of  
>MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the  
>GNU General Public License for more details.  
>  
>You should have received a copy of the GNU General Public License  
>along with this program.  If not, see <http://www.gnu.org/licenses/>.  

## Credits
Coffeenator also makes use of the following projects:  
* [jQuery](http://www.jquery.org/)
* [jQuery User Interface](http://jqueryui.com/)
* [Faenza Icons](http://tiheum.deviantart.com/art/Faenza-Icons-173323228)
* [Django](https://www.djangoproject.com/)
* [Google Visualization API](https://developers.google.com/)

## History
* master - Alpha version in development state.