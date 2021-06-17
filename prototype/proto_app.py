from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import proto_scrape

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/phone_app"
app.config["MONGO_URI"] = "mongodb://localhost:27017/proto_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/phone_app")


@app.route("/")
def index():
    m_data = mongo.db.m_data.find_one()
    return render_template("index.html", m_data=m_data)


@app.route("/scrape")
def scraper():
    m_data = mongo.db.m_data
    m_data_data = proto_scrape.scrape()
    m_data.update({}, m_data_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)