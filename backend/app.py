from flask import Flask
from applicationinsights.flask.ext import AppInsights

# create Flask app
app = Flask(__name__)

app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = 'aea70236-20bd-461b-bc6d-b788fa22d933'
appinsights = AppInsights(app)

# force flushing application insights handler after each request
@app.after_request
def after_request(response):
    appinsights.flush()
    return response

@app.route("/")
def hello_world():
    app.logger.debug('returning hello world')
    return "Hello, World!"


if __name__ == '__main__':
    app.logger.info('Initializing application')
    app.run(port=5050, debug=True, host='0.0.0.0')