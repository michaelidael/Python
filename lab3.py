from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, validators
import requests
import main_functions
import os

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.urandom(24)

class AQIForm(FlaskForm):
    parameter = SelectField('Parameter', choices=[
        ('Air Quality Index', 'Air Quality Index'),
        ('Temperature (C)', 'Temperature (C)'),
        ('Humidity (%)','Humidity (%)'),
        ('Pressure (hPa)', 'Pressure (hPa)')
    ], validators=[validators.DataRequired()])
    submit = SubmitField('Submit')

def get_api_key(filename):
    return main_functions.read_from_file(filename)["aqi_key"]

aqi_key = get_api_key("api_keys.json")




icon_description={
    "01d":"clear sky (day)",
    "01n":"clear sky (night)",
    "02d":"few clouds (day)",
    "02n":"few clouds (night)",
    "03d":"scattered clouds",
    "04d":"broken clouds",
    "09d":"shower rain",
    "10d":"rain (day time)",
    "10n":"rain (night time)",
    "11d":"thunderstorm",
    "13d":"snow",
    "50d":"mist",
}

def get_aqi_data(api_key, parameter):
    url = f"http://api.airvisual.com/v2/nearest_city?key={api_key}"
    response = requests.get(url).json()
    main_functions.save_to_file(response,"aqi_results.json")
    if parameter == "Air Quality Index":
        data = response["data"]["current"]["pollution"]["aqius"]
        unit = ""
    elif parameter == "Temperature (C)":
        data = response["data"]["current"]["weather"]["tp"]
        unit = "ºC"
    elif parameter == "Humidity (%)":
        data = response["data"]["current"]["weather"]["hu"]
        unit = "%"
    elif parameter == "Pressure (hPa)":
        data = response["data"]["current"]["weather"]["pr"]
        unit = "(hPa)"
    else:
        data = "None"
        unit = ""
    city = response["data"]["city"]
    state = response["data"]["state"]
    country = response["data"]["country"]
    icon = response["data"]["current"]["weather"]["ic"]
    return {"data":data,
            "unit":unit,
            "city":city,
            "state":state,
            "country":country,
            "icon_description":icon_description[icon].title(),
            "icon":icon+".png"}

@app.route('/', methods=['GET', 'POST'])
def index():
    form = AQIForm()
    if request.method == "POST":
        parameter_entered = form.parameter.data
        all_data = get_aqi_data(aqi_key, parameter_entered)
        return render_template('aqi_results.html', data=all_data)
    return render_template('aqi.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)