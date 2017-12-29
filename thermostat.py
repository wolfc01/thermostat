from flask import Flask, render_template, jsonify, request, Response
import Queue
import time
import threading

from gevent.pywsgi import WSGIServer
import gevent

app = Flask(__name__)
g_temperature = 0
g_setpoint = 0

@app.route('/')
def main(name=None):
    return render_template('thermostat.html')

@app.route('/adjust', methods=['POST'])
def adjust():
    amount = request.form.get('amount', 0, type=float)
    global g_setpoint
    g_setpoint = g_setpoint + amount
    return jsonify(0)

@app.route("/stream")
def stream():
    def eventStream():
        while True:
          yield "id: {}\ndata:{}\n\n".format("setpoint", g_setpoint)
          yield "id: {}\ndata:{}\n\n".format("temperature", g_temperature)
          gevent.sleep(0.1)  
    return Response(eventStream(), mimetype="text/event-stream")

def thread():
    global g_temperature
    i = 1
    while True:
      g_temperature += 1
      time.sleep(0.1)

if __name__ == "__main__":
  t = threading.Thread(target=thread)
  t.daemon = True
  t.start()
  WSGIServer(("", 8080), app).serve_forever()