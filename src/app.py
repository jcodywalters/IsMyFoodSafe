from flask import Flask, render_template, request
import requests
import datetime
import json


def get_reports(host, query, business_name):
    url = f'https://{host}/resource/gkhn-e8mn.json?{query}&$q="{business_name}"'
    print("fetching url: ", url)
    r = requests.get(url)
    if r.status_code is 200:
        print("success")
        return r.json()
    else:
        print("Not successful")
    return {'error': 'error getting reports ' + r.status_code}


def getUserLocation():
    location_url = 'http://freegeoip.net/json'
    r = requests.get(location_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    location = {'lat': lat, 'lon': lon}
    # location = {'lat': 47.4242534, 'lon': -122.1762584}  // Used for debugging
    print("User Location: ", lat, lon)
    return location


HOST = 'data.kingcounty.gov'
PREVDAYS = 360
BOUND_RANGE = .10
DATERANGE = str(datetime.date.today() - datetime.timedelta(days=PREVDAYS))
USER_LOCATION = getUserLocation()
LAT_LOWER = USER_LOCATION['lat'] - BOUND_RANGE
LAT_UPPER = USER_LOCATION['lat'] + BOUND_RANGE
LON_LOWER = USER_LOCATION['lon'] - BOUND_RANGE
LON_UPPER = USER_LOCATION['lon'] + BOUND_RANGE

FIND_ALL_QUERY = f'$select=name,address,inspection_date,violation_description&violation_type=red&$where=inspection_date>"{DATERANGE}"&$order=inspection_date,address DESC'
FIND_PROXIMITY_QUERY = f'$select=name,address,inspection_date,violation_description&violation_type=red&$where=inspection_date>"{DATERANGE}" AND latitude>{LAT_LOWER} AND latitude<{LAT_UPPER} AND longitude>{LON_LOWER} AND longitude<{LON_UPPER}&$order=inspection_date,address DESC'


app = Flask(__name__)


@app.route('/')
def home_method():
    return render_template('home.html')


@app.route('/', methods=['POST'])
def reports_method():
    business_name = request.form['name']
    if 'button_all' in request.form:
        print('Button - Search All')
        reports = get_reports(HOST, FIND_ALL_QUERY, business_name)
        header_title = "All Reports for " + "'" + business_name + "'"

    if 'button_location' in request.form:
        print('Button - Search User Location')
        reports = get_reports(HOST, FIND_PROXIMITY_QUERY, business_name)
        header_title = "Reports in Proximity for " + "'" + business_name + "'"

    return render_template('home.html', reports=reports, table_header=header_title, show_table=1)

@app.route('/details')
def details():
    return render_template('details.html')


if __name__ == '__main__':
    app.run()
