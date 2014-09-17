RikkaBot
========

RikkaBot is a bot linking Imgur and Gmail, allowing users to send a random
image from a specified imgur album to an email address.

Usage
=====

To use RikkaBot, you'll first need to register the app with both Imgur and 
Google. You can find instructions for Imgur 
[here](https://api.imgur.com/oauth2#register) and Google 
[here](https://developers.google.com/accounts/docs/OAuth2Login#getcredentials).
Then you can run the program with the following command: `python2 main.py`
The arguments for main are as follows:  
imgur-client-id - the client id obtained from registering the app with Imgur  
imgur-client-secret - the client secret id obtained from registering the app 
  with Imgur  
album - the Imgur album to select a random image from  
google-client-id - the client id obtained from registering the app with Google  
google-client-secret - the client secret id obtained from registering the app
  with Google  
to-address - the address to send the email to  
from-address - the address to send the email from  
--data-file - (optional) the file to store imgur and google oauth2 refresh 
  tokens in. Defaults to data.json.  
--header - a header to add before the image link in the email  
--footer - a footer to add after the image link in the email

Dependencies
------------

To use RikkaBot, the following must be installed:  
python2  
The requests library for python2

Developers
==========

Extending
---------

To add new sources for RikkaBot, simply create a subclass of the Source class
and implement the following methods:  
`setUp(self)` - any code that should be executed before `get_message()` 
  or `send_message()`  
`tearDown(self)` - any code that should be executed after `get_message()`
  or `send_message()`  
`get_message(self)` - the code to obtain the message  
`send_message(self, message)` - the code to send the message

Look at lib/google.py and lib/imgur.py for examples.

Tests
-----

To run the provided unittests, cd into the tests directory and run the following
command: `python2 suite.py`. Each test file can also be run individually.
