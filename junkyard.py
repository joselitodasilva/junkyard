from flask import Flask, render_template, Response
import oscserver

app = Flask(__name__)

#ROUTES
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/start")
def start():
	oscserver.start_osc()
	return "osc running"

@app.route("/stop")
def stop():
	oscserver.stop_osc()
	return "osc stopped"


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=1)
