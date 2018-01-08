from flask import Flask, render_template, request
import requests
import datetime

def get_reports(host, query, business_name):
	url = f'https://{host}/resource/gkhn-e8mn.json?{query}&$q="{business_name}"'
	print("fetching url: ", url)
	r = requests.get(url)
	if r.status_code is 200:
		print("success")
		return r.json()
	else:
		print("Not succesful")
	return {'error': 'error getting reports ' + r.status_code}

def get_user_zip():
	geo_url = "http://freegeoip.net/json"
	r = requests.get(geo_url)
	geo_json = r.json()
	return geo_json["zip_code"]

HOST = 'data.kingcounty.gov'
PREVDAYS = 360
USER_ZIP = get_user_zip()
DATERANGE = str(datetime.date.today() - datetime.timedelta(days=PREVDAYS))
QUERY = f'$select=name,address,inspection_date,violation_description&$where=inspection_date>"{DATERANGE}"&violation_type=red&$order=inspection_date,address DESC'

app = Flask(__name__)
app.secrete_key = ""


@app.route('/')
def home_method():
    return render_template('home.html')


@app.route('/result', methods=['POST'])
def reports_method():
	name = request.form['name']
	reports = get_reports(HOST, QUERY, name)
	if (name == ''):
		return render_template('result.html', table_header="No Reports Found", location = USER_ZIP)
	if (len(reports) > 0):
		name = "Reports for " + "'" + name + "'"
		return render_template('result.html', reports=reports, table_header=name, location = USER_ZIP)

	return render_template('result.html', table_header="No Reports Found", location = USER_ZIP)



if __name__ == '__main__':
	app.run()