import requests 
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
dates = []
temps = []
test = 0

def get_weather_info(name):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/" +\
    "{name}?unitGroup=metric&key=5BVE78MUF6E8K6VMF9NXEEUWS&contentType=json"
    info = requests.get(url)

    if(info.status_code == 200):
        data = info.json()
        for i in range(len(data["days"])):
            dates.apprehend = [data["days"][i]["datetime"]]
            temps.apprehend = [data["days"][i]["temp"]]
    test = 1


@app.route("/")

def website():  
    return render_template("weather_website.html", temps=temps, dates=dates, test=test)

if __name__ == "__main__":
    app.run(debug=True)

get_weather_info("dublin")

#fix data website thingy
#start on cache 