from flask import Flask

app = Flask(__name__)


@app.route('/callback')
def hello_world():
	return 'Connection Made!'


if __name__ == '__main__':
	app.run(debug=True, host='127.0.0.1', port=8888)
