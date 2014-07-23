# Django AAF Rapid Connect demo
=========================

Demo of [AAF Rapid Connect](https://rapid.aaf.edu.au/) authentication using Django.

## Register your service

Go to [rapid.aaf.edu.au](https://rapid.aaf.edu.au/) or
[rapid.test.aaf.edu.au](https://rapid.test.aaf.edu.au/) to register
your service's callback URL. This Django site provides a URL of the
form ```http://example.com:8000/rc```. When you register you will
receive a custom AAF authorisation URL, take note of this. Also keep
the secret that you generate.

Note: if you use the test federation then you do not need to set up SSL.

## Install Docker

Install Docker on your Debian host:

    echo deb http://get.docker.io/ubuntu docker main | sudo tee /etc/apt/sources.list.d/docker.list
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
    sudo apt-get update
    sudo apt-get install -y lxc-docker

## Configure the Django site

Clone the repository:

    git clone https://github.com/NIF-au/django-rapid-connect-demo.git
    cd django-rapid-connect-demo

Customise this setting in ```mysite/mysite/settings.py```:

    # Make this unique, and don't share it with anybody.
    SECRET_KEY = 'CHANGE_ME'

Customise the settings in ```mysite/rc/views.py```:

    # The secret that you generated and used when you
    # registered your Rapid Connect service.
    secret = "SECRET_CHANGE_ME"

    # The authorisation URL that AAF provided.
    url = 'CHANGE_ME'

    # Issuer is either 'https://rapid.test.aaf.edu.au' or 'https://rapid.aaf.edu.au'
    # and the audience is the URL of your site that you registered with AAF.
    config = {}
    config['test.aaf.edu.au'] = {
      'iss': 'https://rapid.test.aaf.edu.au',
      'aud': 'CHANGE_ME',
    }

Build the Docker image:

    sudo docker build -t='user/django-aaf-rc' .

The passwords for the django superuser and admin user are randomly
generated, so take note of them during in the build output:

     ---> Running in 1d21a78b631e
    Superuser created successfully.
    Changing password for user 'superuser'
    Password changed successfully for user 'superuser'
    Django superuser password: XXXXXXXXXXXXXXXXXXXX
    Django admin password: YYYYYYYYYYYYYYYYYYYY

## Run it

    sudo docker run -i -t --rm -p 0.0.0.0:8000:8000 user/django-aaf-rc

The argument ```0.0.0.0:8000:8000``` is of the form ```<listen host>:<host port>:<container port>```.

To poke around in the container, run a shell:

    sudo docker run -i -t --rm -p 0.0.0.0:8000:8000 user/django-aaf-rc /bin/bash

but beware that changes are lost by default when the container exits,
as usual with a Docker container workflow.

Open http://example.com:8000/rc/

1. Click the big orange button.
2. Choose your institution on the AAF site.
3. Log in using your institution's single sign-on service.
4. Finally, you will be redirected to the protected URL ```/rc/welcome``` which displays the attributes
received from the AAF service:

    Success! You have been authenticated via AAF's Rapid Connect service!

    Here is everything in the session dict:



    edupersontargetedid: https://rapid.test.aaf.edu.au!http://XXX.XXX.XXX.XXX:8000/rc/XXXXXXXXXXXXXXXXXXXXXXXXXXXXX 
    displayname: Dr Carlo Hamalainen 
    cn: Carlo Hamalainen 
    edupersonscopedaffiliation: staff@uq.edu.au 
    edupersonprincipalname: XXXXXXXXXXX@uq.edu.au 
    mail: c.hamalainen@uq.edu.au 
    surname: Hamalainen 
    givenname: Carlo 


    Hey, you could pop over to the django admin interface using your newly created AAF identity!

    For example, look at the admin/user page.

    Logout from this site (your institution single-sign-on session will be active until you close your browser session).

At this point the user is authenticated against Django's auth system, so navigating to
```/admin``` shows the Django admin interface and the user does not need to log in.

