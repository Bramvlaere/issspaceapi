import requests
import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request


app = Flask(__name__)
load_dotenv()
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/find_iss', methods = ['POST', 'GET'])
def index():

    if request.method == 'POST':
        access_token = os.getenv("ACCESS_TOKEN")
        response = requests.get(os.getenv('URL'))
        latitude = response.json()['iss_position']['latitude']
        longitude = response.json()['iss_position']['longitude']

        Location_format_q = {"key": access_token, "lon": longitude, "lat": latitude, "format": "json"}
        Location_format_res = requests.get(os.getenv("LOCATION_URL"), params = Location_format_q).json()
        
        if 'error' in Location_format_res:
            res='in space you dummy'
            return render_template('results.html', res=res)
        
        res = {
            'location': Location_format_res['address']['country']
        }
        print(Location_format_res)
        return render_template('results.html', **res)
    return render_template('find_iss.html')

@app.route('/inspace', methods = ['POST', 'GET'])
def in_space():
    if request.method == 'POST':
        response = requests.get(os.getenv('PPL_IN_SPACE'))
        people_in_space = response.json()['number']
        reply = {'number' : people_in_space}
        return render_template('inspace.html', **reply)
    return render_template('people_in_space.html')


if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 8100, debug = True)
