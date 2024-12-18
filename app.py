# app.py
from flask import Flask, render_template
from flask_cors import CORS
import routes  # Ensure routes.py is in the same directory

app = Flask(__name__)
CORS(app)

# Register the Blueprint
app.register_blueprint(routes.api, url_prefix='/api')

@app.route('/')
def home():
    # Make sure templates/index.html exists
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
