import os
from flask import Flask,redirect,url_for,render_template,request, send_from_directory, abort, flash,jsonify 
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt
from bson import json_util
import json
from glob import glob
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3



app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/music_radio_project"
mongodb_client = PyMongo(app)
db = mongodb_client.db

@app.route('/',methods=['GET', 'POST'])
def sign():
    if request.method=='POST':
        x = request.form['email']
        y = request.form['password']
        print(x,y)
        user = db.user.find_one({'email' :x, 'password':y})
        print(user)
        if user != None :
           firstname =  user['firstName']
           lastname = user['lastName']
           print(firstname)
           return redirect(url_for('home',firstname=firstname))
    return render_template("Sign.html")

@app.route('/password',methods=['GET', 'POST'])
def password():
    if request.method=='POST':
        x = request.form['email']
        y = request.form['password']
        print(x,y)
        user = db.user.find_one({'email' :x})
        print(user)
        if user != None :
           db.user.replace_one({'email': x}, {'firstName':user["firstName"],'lastName':user["lastName"],'email': user["email"], 'password': y })
           print("done")
           return redirect(url_for('home', USER=user))
        else:
            return redirect(url_for('sign'))
    return render_template("password.html")


@app.route("/account",methods=['GET','POST'])
def account():
    if request.method=='POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        print( firstName,lastName,email,password)
        db.user.insert_one({'firstName': firstName, 'lastName':lastName , 'email': email, 'password':password})

        user = db.user.find_one({'firstName': firstName, 'lastName':lastName , 'email': email, 'password':password})
        if user != None :
           print('done')
           return redirect(url_for('home', USER=user["firstName"]))
    return render_template("NewAccount.html")

@app.route("/home",methods=['GET','POST'])

def home():
    images = []
    musics = db.music.find()
    for i in musics:
      images.append(i['image'])
    print(images)

    songs = []
    musics = db.music.find()
    for i in musics:
       songs.append(i['song'])
    return render_template("home2.html")


app.run(host='127.0.0.2',port=8000,debug=True)