from dummy_sensors import init_app
import os


app = init_app()

if __name__ == "__main__":
    # print(os.getpid())
    app.run(host="0.0.0.0", debug=False, port=26223, use_reloader=False)
