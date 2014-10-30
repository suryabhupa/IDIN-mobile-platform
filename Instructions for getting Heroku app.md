Web app for the IDIN mobile platform
====================================

Commands to try in this order:
-------------------------------

$ heroku login
(...enter your Heroku credentials...)

$ git heroku git:clone -a twilio-messenger
[if this works, then you are all set!]


Fixes:
------
Follow the instructions on this page:
https://devcenter.heroku.com/articles/keys

At some point, you might have to make a new SSH pub/private key set, and have the directory be something like 

/Users/surya/.ssh/[name]

and in their example, they have that [name] = id.heroku; after this, make sure you 

$ heroku add:keys

and select the new one you just made as id.heroku, and then check:

$ ssh -v git@heroku.com

and if this works, then you can go back to the very top and try again! :) 

