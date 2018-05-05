from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app)

@app.route("/")
def index():
    datas = mongo.db.marsdata.find()
    for data in datas:
        print(data)
    return render_template("index.html", dataforsite=datas)
@app.route("/clear")
def clear():
    result = db.marsdata.delete_many({})
    datas=db.marsdata.find()
    return redirect("http://127.0.0.1:5000/", code=302)
   

@app.route("/scrape")
def scrape():
    data = scrape_mars.scrape()
    mongo.db.marsdata.insert_many(data)
   
 
    return redirect("http://127.0.0.1:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
