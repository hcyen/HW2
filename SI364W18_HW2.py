## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file
## (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the
## routes described in the README exist and render the templates they are supposed to
## (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.
# https://developer.apple.com/library/content/documentation/AudioVideo/Conceptual/iTuneSearchAPI/Searching.html#//apple_ref/doc/uid/TP40017632-CH5-SW1
# https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/

# https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/GetaSingleArtist.html#//apple_ref/doc/uid/TP40017625-CH9-SW1
#############################
##### IMPORT STATEMENTS #####
#############################
import os
import urllib
import re
import datetime
import json
import urllib.request, urllib.parse, urllib.error
from urllib.request import Request, urlopen
import ssl
import requests
import pprint
from flask import Flask, request, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import TextField, StringField, SubmitField, RadioField, ValidationError
from wtforms import validators
from wtforms.validators import Required
#from forms import AlbumEntryForm
from flask import flash



#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################
#http://wtforms.readthedocs.io/en/latest/fields.html
#The form and class are defined in forms.py
'''
class AlbumEntryForm(FlaskForm):
   albumname = StringField("Enter the name of an album:",[validators.Required("Please enter the album name.")])
   howmuchlike = RadioField('How much do you like this album? (1 low, 3 high)', choices = [('1','1'),('2','2'),('3','3'),[validators.Required("Please select one.")]])
   
   submit = SubmitField("Send")
'''
#https://stackoverflow.com/questions/14591202/how-to-make-a-radiofield-in-flask
#https://stackoverflow.com/questions/40986924/render-flask-wtforms-radiofield-lines-buttons-in-an-ordered-list
#https://stackoverflow.com/questions/27705968/flask-wtform-radiofield-label-does-not-render
class AlbumEntryForm(FlaskForm):
   #albumname = StringField("Enter the name of an album:",[validators.Required("Please enter the album name.")])
   albumname = TextField("Enter the name of an album:",[validators.Required("Please enter the album name.")])
   howmuchlike = RadioField('How much do you like this album? (1 low, 3 high)', choices = [('1','1'),('2','2'),('3','3')] ,default='2',validators=[Required()]) #in choices, first num = value, second num is what is displayed in HTML file
   #[validators.Required("Please select one.")]])
   
   submit = SubmitField("Submit")


####################
###### ROUTES ######
####################


@app.route('/') #'/' signifies top route directory
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>') #<name> = parameter within URL
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name) #0 = index for first parameter


@app.route('/artistform')
def itunesartistform():
    
        return render_template('artistform.html')

@app.route('/artistinfo', methods = ['POST', 'GET']) #two options
def itunesartistinfos():
    #title = "My Ice Cream Form"
    # Add code -- what type should options hold?
    if request.method == 'POST':
        result = request.form['artist'] #artist, name identifier for textbox for /artistform #.form obtains value of POST/GET request variable 
        #https://itunes.apple.com/search?term=jack+johnson&media=music #get .json txt file download
        baseurl = "https://itunes.apple.com/search" #itunes search api
        params_diction = {} #initialize as dictionary 
        params_diction["term"] = result  #result = request.form['artist'] 
        params_diction["media"] = 'music' #limiter for media type
    
        resp = requests.get(baseurl,params=params_diction) 
        text = resp.text 
        py_objects = json.loads(text) #turn text value into json file
        typ_obj = type(py_objects) 
        print(type(py_objects)) 
        objects = py_objects["results"] #results - whatever people search up in artist text box 
        print(objects) #print value of objects

    else:
        result = request.args.get('artist') 
        baseurl = "https://itunes.apple.com/search"
        params_diction = {}
        params_diction["term"] = result
        params_diction["media"] = 'music'
    
        resp = requests.get(baseurl,params=params_diction)
        text = resp.text
        py_objects = json.loads(text)
        typ_obj = type(py_objects)
        objects = py_objects["results"]
        print(objects)
        
    return render_template('artist_info.html', objects=objects) #parameter name objects is set as 'objects' defined in function
    # the first/left objects is the variable from the artist_info.html and the second/right objects is the variable from this function
    # SI364 Section W3 | Jan 15-16 | Templates, More Practice - Diagramming Task 1
    #return redirect(url_for('artistinfo'))
    #return redirect(url_for('artistinfo', name = res))


#https://stackoverflow.com/questions/21499265/itunes-music-track-view-url-open-error

@app.route('/artistlinks')
def itunesartistlinks():
    #title = "My Ice Cream Form"
    # Add code -- what type should options hold?
    return render_template('artist_links.html')

#https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/GetaSingleArtist.html
@app.route('/specific/song/<artist_name>')
def itunesspecificartist(artist_name): #artist_name = parameter for URL
    baseurl = "https://itunes.apple.com/search"
    params_diction = {}
    params_diction["term"] = artist_name
    params_diction["media"] = 'music'
    resp = requests.get(baseurl,params=params_diction)
    text = resp.text
    python_obj = json.loads(text)
    results = python_obj["results"]
    
    
    return render_template('specific_artist.html', results=results)
    ## the first/left results is the variable from the specific_artist.html and the second results is the variable from this function

# for the album_entry.html parameters
#https://stackoverflow.com/questions/14591202/how-to-make-a-radiofield-in-flask 
#http://wtforms.readthedocs.io/en/latest/fields.html
# when type http://localhost:5000/album_entry, always got this ValueError: not enough values to unpack (expected 2, got 1)
# the reason is due to the template html - album_entry.html has the wrong parameter style for the radiofield
# this doc suggests the following http://wtforms.readthedocs.io/en/latest/fields.html#wtforms.fields.RadioField
# {% for subfield in form.radio %}
#    <tr>
#        <td>{{ subfield }}</td>
#        <td>{{ subfield.label }}</td>
#    </tr>
# {% endfor %}
# but it is wrong. should simply like this
#                                <tr>
#					<td>{{ form.howmuchlike.label }}</td>
#					<td>{{ form.howmuchlike }}</td>
#				</tr>
@app.route('/album_entry', methods = ['POST', 'GET'])
#@app.route('/album_entry')
def albumentry():
   form = AlbumEntryForm()
   return render_template('album_entry.html', form = form)
   
   '''if request.method == 'POST':
      if form.validate() == False:
         flash('All fields are required.')
         return render_template('album_entry.html', form = form)
      else:
         return render_template('album_entry.html', form = form)
         #return "Sorry, no data available"
   elif request.method == 'GET':

        return render_template('album_entry.html', form = form)'''
    
@app.route('/album_result', methods = ['POST', 'GET'])
def albumdata():
    form = AlbumEntryForm()
    if form.validate_on_submit():
        album_name = form.albumname.data
        how_much_like = form.howmuchlike.data
        print(form.howmuchlike.data)
        return render_template('album_data.html', albumname=album_name, howmuchlike=how_much_like)
        #return render_template('album_data.html', albumname=album_name)

    return "Sorry, no data available"
        
if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
