from server import init_app


app = init_app()

if __name__ == "__main__":
    app.run(host='localhost', debug=True)
    # app.run(host='0.0.0.0', debug=True, ssl_context='adhoc', port=5500)
