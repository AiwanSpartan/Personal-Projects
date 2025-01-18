import requests 
import os 
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, reqparse, Resource
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weather_data.db"
db = SQLAlchemy(app)
dates = []
temps = []
user_input = ""
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
api = Api(app)

def get_weather_info(name):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/" \
    f"timeline/{name}?unitGroup=metric&key={WEATHER_API_KEY}&contentType=json"

    info = requests.get(url)

    if(info.status_code == 200):
        data = info.json()
        for i in range(len(data["days"])):
            date = datetime.strptime(data["days"][i]["datetime"], "%Y-%m-%d")
            dates.append(date)
            temps.append(data["days"][i]["temp"])

    else:
        return "nothing"

#home page
@app.route("/")
def home():  
    return render_template("weather_website.html")

class CityData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    town = db.Column(db.String(100), nullable=False)
    dates = db.Column(db.Date, nullable=False)
    temps = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Weather info for Town : {user_input}, {self.dates} and {self.temps}"
    
user_args = reqparse.RequestParser()

#page after input 
@app.route("/button", methods=["POST"])
def button_pressed():
    user_input = request.form.get("inputted_city")
    get_weather_info(user_input)  

    # Insert each date-temp pair into the database
    for date, temp in zip(dates, temps):
        new_data = CityData(town=user_input, dates=date, temps=temp)
        db.session.add(new_data)

    db.session.commit() 
    return render_template("weather_website.html", list_of_temps=temps, list_of_dates=dates)

#get data
@app.route('/get_data', methods=['GET'])
class CityDataResource(Resource):
    def get(self):
        # Query all data from CityData model
        data = CityData.query.all()
        
        # Prepare data to send back in response
        result = []
        for row in data:
            result.append({
                'town': row.town,
                'dates': row.dates.strftime('%Y-%m-%d'),  # Format date as a string
                'temps': row.temps
            })
        
        return jsonify(result)  # Return the data as JSON response


api.add_resource(CityDataResource, "/api/weatherPage/")

if __name__ == "__main__":
    app.run(debug=True)

#find a way to store user data 
#start on cache 
#error handling 
#multiple buttons/webpages implement jaavscript and AJAX 