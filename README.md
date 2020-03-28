# Setting Up templog flask app using Ubuntu virtual machine on Amazon Lightsail

The templogclient needs to communicate with the templog flask app at a static IP address using HTTP. This would be possible 
to define on a home network or possibly within a VPN.  Domestic ISPs do not seem to offer a static IP as standard and using 
dynamic DNS seemed to be a bit too complicated. My objective in designing the code was to enable an organisation with 
different geographic settings to deploy the templogclient on a raspberry pi zero w to measure fridge temperatures, reporting 
minute by minute to the templog app what the sensed temperature is. There would always be a power source present because of
the fridge. The Pi Zero W has wifi built in: I assumed the organisation would have a wifi network.
The app calculates the maximum and minimum recorded temperature in each location per 24 hour period and stores it in a 
database which, with password protection, can be viewed in a web browser at the IP address where the app is hosted.  
Please feel free to fork the code and credit me where appropriate.

I have relied on Miguel Grinbergs excellent Flask blog to create this code and what follows  are instructions paraphrased from: 
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux
https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https

Other sources consulted include:
Steve Breuning's reaspberrywebserver http://raspberrywebserver.com/ 
Harry's Developer blog https://wingoodharry.wordpress.com/


Instructions are given for Amazon Lightsail as a cost effective option that I did manage to get up and running.

*Sign up for lightsail account

https://aws.amazon.com/lightsail/

*Assign static IP to instance 

*Open firewall ports on aws dashboard

22, 80, 443

*Connect via SSH 

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html

*Buy a domain name and configure A setting to redirect to your static IP

# Configure software to serve templog app

*Create a User other than root for security

      $ adduser --gecos "" templogger

      $ usermod -aG sudo templogger

      $ su templogger


*Copy public ssh cert for no password login

Local machine check for keys

    $ ls ~/.ssh

If keys present will list id_rsa.pub

If not run

    $ ssh-keygen

    $ cat ~/.ssh/id_rsa.pub

Copy the whole output and paste to remote (Lightsail) terminal in place of <paste key> on line 67.

    $ echo <paste key> >> ~/.ssh/authorized_keys

    $ chmod 600 ~/.ssh/authorized_keys

log out of templogger user

    $ exit

log out of root user

    $ exit

*Stop root log in for security

log back in without password

    $ ssh templogger@<server-ip-address>

    $ sudo nano /etc/ssh/sshd_config

PermitRootLogin no

PasswordAuthentication no

    $ sudo service ssh restart


*Firewall

    $ sudo apt-get install -y ufw
    $ sudo ufw allow ssh
    $ sudo ufw allow http
    $ sudo ufw allow 443/tcp
    $ sudo ufw --force enable
    $ sudo ufw status

*base dependencies

    $ sudo apt-get -y update
    $ sudo apt-get -y install python3 python3-venv python3-dev
    $ sudo apt-get -y install supervisor nginx git

*git clone

    $ git clone https://github.com/ROBrownsmith/templog.git
    $ cd templog

*venv 

    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt

* install Gunicorn

      (venv) $ pip install gunicorn

exit venv

    exit

*edit .env file secret key for security

    $ python3 -c "import uuid; print(uuid.uuid4().hex)”

copy the output

    $ sudo nano ~/templog/.env

paste into line 1 where indicated, save, then exit.

*Set FLASK_APP environment variable for temp logger account

    $ echo "export FLASK_APP=microblog.py" >> ~/.profile

    $ exit

log back in again

*database

    $ cd templog

    $ source venv/bin/activate

    (venv) $ flask db upgrade

*Gunicorn use with 1 worker

    $ sudo cp /home/templogger/templog/conf_files/templog.conf  /etc/supervisor/conf.d/templog.conf

    $ sudo supervisorctl reload

*Nginx

    $ sudo rm /etc/nginx/sites-enabled/default

    $ sudo cp /home/templogger/templog/conf_files/templog /etc/nginx/sites-enabled/templog

edit the file at line 5 and 18 to include your own domain

    $ sudo nano /etc/nginx/sites-enabled/templog

*insert users into Database

instructions for adding users to sqlite tables pending
