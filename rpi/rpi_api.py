from flask import Flask
from flask_cors import CORS, cross_origin

import subprocess

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/reboot')
@cross_origin()
def reboot():
    if subprocess.run('reboot', shell=True, stdout=subprocess.DEVNULL).returncode == 0:
        return 'OK'
    else:
        return 'NOK'

@app.route('/shutdown')
@cross_origin()
def shutdown():
    if subprocess.run('shutdown now', shell=True, stdout=subprocess.DEVNULL).returncode == 0:
        return 'OK'
    else:
        return 'NOK'


if __name__ == '__main__':
    app.run(host='0.0.0.0')


