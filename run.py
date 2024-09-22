from poller import poller_api
from poller.api.routes.main import register as register_main


app = poller_api()

register_main(app)


if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0', port=5050)