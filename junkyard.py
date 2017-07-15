from flask import Flask, render_template, Response
import junkberry

app = Flask(__name__)

#me = junkberry.junkberry()
#me.defineType()
#print me.type

print junkberry.device


#ROUTES
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/start")
def start():
	#oscserver.start_osc()
	junkberry.osc("run")
	return "osc running"

@app.route("/stop")
def stop():
	junkberry.osc("stop")
	return "osc stopped"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=1)
