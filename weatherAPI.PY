import requests 
import os 
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
dates = []
temps = []
user_input = ""
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather_info(name):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/" \
    f"timeline/{name}?unitGroup=metric&key={WEATHER_API_KEY}&contentType=json"

    info = requests.get(url)

    if(info.status_code == 200):
        data = info.json()
        for i in range(len(data["days"])):
            dates.append(data["days"][i]["datetime"])
            temps.append(data["days"][i]["temp"])

    else:
        return "nothing"

@app.route("/")
def home():  
    return render_template("weather_website.html")

@app.route("/button", methods=["POST"])
def button_pressed():
    user_input = request.form.get("inputted_city")
    get_weather_info(user_input)
    return render_template("weather_website.html", list_of_temps=temps, list_of_dates=dates)

if __name__ == "__main__":
    app.run(debug=True)

#start on cache 
#error handling 
#multiple buttons/webpages implement jaavscript and AJAX 