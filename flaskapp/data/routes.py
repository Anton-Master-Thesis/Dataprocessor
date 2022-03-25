from flaskapp import app

@app.route("/")
def index():
    return "Test"

@app.route("/test/data")
def testData():
    return "data"