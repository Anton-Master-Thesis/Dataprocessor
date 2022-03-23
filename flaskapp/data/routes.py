from flaskapp import app

@app.route("/")
def index():
    return "Test"