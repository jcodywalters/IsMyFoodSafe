from flask import Flask, render_template, request
import requests
import datetime

HOST = 'data.kingcounty.gov'
PREVDAYS = 360
DATERANGE = str(datetime.date.today() - datetime.timedelta(days=PREVDAYS))
QUERY = f'$select=name,address, inspection_date,violation_description&$where=inspection_date>"{DATERANGE}"&violation_type=red&$q="'


def get_reports(host, query, business_name):
	url = f'https://{host}/resource/gkhn-e8mn.json?{query}{business_name}"&$order=inspection_date,address DESC'
	print(url)
	r = requests.get(url)
	if r.status_code is 200:
		print("success")
		return r.json()
	else:
		print("Not succesful")
	return {'error': 'error getting reports ' + r.status_code}




app = Flask(__name__)
app.secrete_key = "hello"


@app.route('/')
def home_method():
    return render_template('home.html')


@app.route('/result', methods=['POST'])
def reports_method():
	name = request.form['name']
	reports = get_reports(HOST, QUERY, name)
	if (name == ''):
		return render_template('result.html', reports="No Reports Found")
	if (len(reports) > 0):
		return render_template('result.html', reports=reports, name=name)

	return render_template('result.html', reports="No Reports Found")



if __name__ == '__main__':
	app.run()