from flask import Flask
from ..APIs import ratepackage, packagebyname, auth, packageid
from flask_cors import CORS

app = Flask(__name__)
app.json.sort_keys = False  # Keeps the JSON output in the same order as the database
app.register_blueprint(ratepackage.bp)
app.register_blueprint(packagebyname.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(packageid.bp)
CORS(app)

if __name__ == '__main__':
    app.run()