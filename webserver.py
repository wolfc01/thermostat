from flask import Flask, render_template, jsonify, request, Response
import Queue
import time
import threading
import os
import sys

from gevent.pywsgi import WSGIServer
import gevent

import globals

app = Flask(__name__)
g_temperature = 0
g_setpoint = 0
g_stop = False

@app.route('/')
def main(name=None):
  return render_template('thermostat.html')

@app.route('/adjust', methods=['POST'])
def adjust():
  amount = request.form.get('amount', 0, type=float)
  global g_setpoint
  g_setpoint = g_setpoint + amount
  globals.writefifo(globals.FIFO_SETPOINT, globals.COMMAND_NEWSETPOINT, str(g_setpoint))
  return jsonify(0)

@app.route("/stream")
def stream():
  def eventStream():
    while True:
      yield "id: {}\ndata:{}\n\n".format("setpoint", g_setpoint)
      yield "id: {}\ndata:{:2.2f}\n\n".format("temperature", g_temperature)
      gevent.sleep(0.1)  
  return Response(eventStream(), mimetype="text/event-stream")

def thread():
  global g_stop
  while g_stop == False:
    global g_temperature
    command, value = globals.readfifo(globals.FIFO_ACTUALWEBSERVER).split(":")
    if command == globals.COMMAND_NEWACTUAL:
      g_temperature = float(value)
    time.sleep(0.1)

if __name__ == "__main__":
  try:
    t = threading.Thread(target=thread)
    t.daemon = True
    t.start()
    WSGIServer(("", 8080), app).serve_forever()
  except KeyboardInterrupt:
    g_stop = True
    t.join()
    sys.exit(0)