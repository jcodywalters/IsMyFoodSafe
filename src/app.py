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

# Query issue when pushed to Heroku. Using different query to return answer for now
# QUERY = f'$select=name,address,inspection_date,violation_description&violation_type=red&$where=inspection_date>"{DATERANGE}" AND latitude>{LAT_LOWER} AND latitude<{LAT_UPPER} AND longitude>{LON_LOWER} AND longitude<{LON_UPPER}&$order=inspection_date,address DESC'
QUERY = f'$select=name,address,inspection_date,violation_description&violation_type=red&$where=inspection_date>"{DATERANGE}"&$order=inspection_date,address DESC'


app = Flask(__name__)
app.secrete_key = ""


@app.route('/')
def home_method():
    return render_template('home.html')


@app.route('/result', methods=['POST'])
def reports_method():
    businessName = request.form['name']
    reports = get_reports(HOST, QUERY, businessName)
    if (businessName == ''):
        return render_template('result.html', table_header="No Reports Found")
    # if (len(reports) > 0):
    name = "Reports for " + "'" + businessName + "'"
    return render_template('result.html', reports=reports, table_header=businessName)

    # return render_template('result.html', table_header="No Reports Found")


if __name__ == '__main__':
    app.run()
