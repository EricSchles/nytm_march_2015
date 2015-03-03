from flask import Flask, render_template, redirect,request,url_for
from data_grab import Scraper
import pickle
import investigate
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    #connections found between ads
    #keywords found
    return render_template("index.html")

@app.route("/investigate",methods=["GET","POST"])
def investigator():
    password = request.form.get("password")
    running = request.form.get("long_running")
    if password == "like_i_d_tell_you":
        if running == "long":
            investigate.run()
        else:
            investigate.run(long_running=False)
    return redirect(url_for("index"))

@app.route("/add",methods=["GET","POST"])
def add():
    return render_template("add.html")

@app.route("/add_data",methods=["GET","POST"])
def add_data():
    investigation_type = request.form.get("investigation_type")
    url = request.form.get("url_list")
    urls = url.split(",")
    scraper = Scraper()
    data = scraper.scrape(links=urls,auto_learn=True)
    if investigation_type == "directed":
        keywords = pickle.load( open("keywords.p", "rb"))
        for datum in data:
            keywords += datum["new_keywords"]
        pickle.dump(keywords, open("keywords.p","wb"))
    elif investigation_type == "undirected":
        train = pickle.load( open("train.p","rb"))
        for datum in data:
            train.append((datum["text_body"],"trafficking"))
        pickle.dump( train, open("train.p","wb") )
    return redirect(url_for("index"))

app.run(debug=True)
