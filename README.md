# Spatify

## Dependencies Needed

* spotipy
* requests
* flask
* python 3
* celery
* redis/redis-server

## Running the Program

You will ned to have a spotify account in order to use
this program. Once you have created a spotify account,
then you will need to register your application in order
to get a client id and client secret. Follow this link
to do so.

> https://developer.spotify.com/web-api/tutorial/

After cloning the repository from git, you will need
to run the flask_app.py file so that spotify can use
it as a redirct uri using this command.

> python3 flask_app.py

Once the flask app is running, then you can run the
api_connection.py file to create the initial connection
to spotify. You must run this command.

> python3 api_connection.py

Once it starts running to will redirect you to a web
page that will prompt you to login to your spotify account.
After logging, the page will be redirected again to another
page. You must copy the url from this page and paste it
into the command line where the prompt should be waiting
for you to paste in the url received. Once this is done,
the api_connection.py file should complete execution.
This whole process only needs to be done one time to
establish the connection to spotify that gives you the
access token needed to run queries against the spatify
api. There will be .cache-< your spotify username > file
that is created which holds the access token and the
fresh token. Do not delete this file, it is important.
