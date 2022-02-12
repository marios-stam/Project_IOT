from http.client import GATEWAY_TIMEOUT
from dummy_sensors import init_app


app, gateway = init_app()

if __name__ == "__main__":
    gateway.start_processes()
    app.run(host="0.0.0.0", debug=True, port=26223)
