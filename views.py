# This component handles outbound messaging.

from flask import render_template, request
from flask.ext.restless import APIManager
from app import app, db
from models import Message


#from flask import Flask, render_template, request, redirect, make_response
#from flask.ext.sqlalchemy import SQLAlchemy
from twilio.rest import TwilioRestClient
##from bottle import run, request, HTTPResponse
import twilio.twiml
import sendgrid
import json
import plivo
import plivoxml as XML
import requests

import os

if os.environ.has_key('twilio_account') and os.environ.has_key('twilio_token') and os.environ.has_key('SENDGRID_USERNAME') and os.environ.has_key('SENDGRID_PASSWORD'):
    account = os.environ['twilio_account']
    token = os.environ['twilio_token']
    username = os.environ['SENDGRID_USERNAME']
    password = os.environ['SENDGRID_PASSWORD']
    placcount = os.environ['plivo_account']
    pltoken = os.environ['plivo_token']

else:
    from local_settings import *

from models import Message

client = TwilioRestClient(account, token)
sendgrid_api = sendgrid.SendGridClient(username, password)
plivo_api = plivo.RestAPI(placcount, pltoken)

#plivo_number = 14842027664
plivo_number = "14842027664"


#REST API

manager = APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Message, methods=['GET'])

@app.route('/')
def ReturnForm():
  # for sms in client.sms.messages.list():
    #print "From: " + sms.from_formatted + "To: " + sms.to_formatted
  #smss = client.sms.messages.list()
  #print smss.html
  return render_template('form.html')

@app.route('/', methods=['GET','POST'])
def FormPost():
  sendto = request.form['to-number']
  at_symbol = "@"
  brazil_code = "+55"
  usa_code = "+1"
  if at_symbol in sendto:
    message = sendgrid.Mail(to=request.form['to-number'], subject='Test email from IDIN web app', html=request.form['Message'], text=request.form['Message'], from_email='16176064716@sms.idinmessagetest.cf')
    status, msg = sendgrid_api.send(message)

  #if brazil_code in sendto:
  else:
      text = request.form['Message']
      message_params = {
        'src':plivo_number,
        'dst':sendto,
        'text':text}
      print plivo_api.send_message(message_params)
      m = Message(to_number=message_params['dst'],
      from_number=message_params['src'], text=message_params['text'])
      db.session.add(m)
      db.session.commit()
      #return render_template('success.html')
      #return render_template('table.html')
      #Return the form and the messages so far

  #if usa_code in sendto:
  #    text = request.form['Message']
  #    message_params = {
  #      'src':plivo_number,
  #      'dst':sendto,
  #      'text':text}
  #    print plivo_api.send_message(message_params)
  #    m = Message(to_number=message_params['dst'],
  #    from_number=message_params['src'], text=message_params['text'])
  #    db.session.add(m)
  #    db.session.commit()
      #return render_template('success.html')
      #return render_template('table.html')
  #else:
  #  message = client.sms.messages.create(to=request.form['to-number'], from_="+16176064716", body=request.form['Message'])
  #  m = Message(to_number=request.form['to-number'], from_number="+16176064716", text=request.form['Message'])
  #  db.session.add(m)
  #  db.session.commit()
    #return render_template('success.html')
    #return render_template('table.html')
		#msgs = query_db('select text from messages;')

  messages = Message.query.all()
  return render_template('table.html', messages=messages)

# This component handles incoming messages.

callers = {
  "+18179460792": "Amber",
  "+5511982023271": "Miguel",
  "+13474462905": "Jona"
}

@app.route("/handle-sms", methods=['GET', 'POST'])
def response_text():
  from_number = request.values.get('From', '')
  print "received sms"
  print "From: ", from_number
  params = {
  'src': plivo_number, # Caller Id
  'dst' : from_number, # User Number to Call
  'text' : "It works! Hello.",
  'type' : "sms",
  }

  recd = Message(to_number=params['src'], from_number=params['dst'], text=request.values.get('Text', ''))
  db.session.add(recd)
  db.session.commit()

  response = plivo_api.send_message(params)

  autresp = Message(to_number=params['dst'], from_number=params['src'], text=params['text'])
  db.session.add(autresp)
  db.session.commit()
  return "success"
  #return str(response)

  #  if from_number in callers:
  #      response_text = "Hi " + callers[from_number] + ", thanks for the message!"
  #  else: response_text = "Hello! Thank you for the message!"    
  #  

  #response_text = "Good day, sir!"
  #r = plivo.XML.Response()
  #r.addMessage(response_text, src=plivo_number, dst=from_number)
  ##resp = r.to_xml()
  #print resp
  #return r
#
#  resp = twilio.twiml.Response()
#  resp.message(response_text)
#  return str(resp)
#

  #params = {
  #'src': '14842027664', # Caller Id
  #'dst' : '18179460792', # User Number to Call
  #'text' : "Hi, message from Plivo",
  #'type' : "sms",
  #}
  
#@app.route('/handle-sms', methods=['POST']) 
#def hello(): 
#    Text = request.forms.get('Text')
#    From = request.forms.get('From')
#    print "Message received: %s - by %s" % (Text, From)
#    return HTTPResponse(status=200)

 
