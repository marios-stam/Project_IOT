from dummy_sensors import init_app
from dummy_sensors.sensor_resources import gateway


app = init_app()

if __name__ == "__main__":
    gateway.start_processes()
    app.run(host="0.0.0.0", debug=True, port=26223)
