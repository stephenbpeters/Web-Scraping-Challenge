from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import proto_scrape

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/phone_app"
app.config["MONGO_URI"] = "mongodb://localhost:27017/proto_app"
mongo = PyMongo(app)
m_data = mongo.db.m_data

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/phone_app")


@app.route("/")
def index():
    db_data = m_data.find_one()
    return render_template("index.html", m_data=db_data)


@app.route("/scrape")
def scraper():
    scraped_data = proto_scrape.scrape()
    m_data.update({}, scraped_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)