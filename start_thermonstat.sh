if [ -d ".venv" ]; then
  . venv/bin/activate
fi
export FLASK_APP=thermostat.py
export FLASK_DEBUG=1
python thermostat.py


