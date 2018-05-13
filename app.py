
#go to this file in terminal, run it (python app.py); then go to localhost:5000 in chrome to view
# make sure when done, type Ctrl C in terminal to quit the app..
#make sure you have mongo db open in terminal as well, 'mongod'

from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars_two

app = Flask(__name__)

mongo = PyMongo(app)# this is naming the mongo db 'app'

@app.route("/")
def index():
    datas = mongo.db.marsdata.find_one()
    if (not datas):#if there's no db found, then will still run, and allow index page to render and scrape
        datas=[]
    for data in datas:
         print(datas)#prints to console for debugging
    return render_template("index.html", dataforsite=datas)

@app.route("/clear")
def clear():
    result = mongo.db.marsdata.delete_many({})
    datas=mongo.db.marsdata.find()
    return redirect("http://127.0.0.1:5000/", code=302)
   

@app.route("/scrape")
def scrape():
    mongo.db.marsdata.drop()
    data = scrape_mars_two.scrape()
    mongo.db.marsdata.insert_one(data)
   
 
    return redirect("http://127.0.0.1:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
