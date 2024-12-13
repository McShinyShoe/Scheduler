from flask import Flask
from routes import configure_routes

# Get Flask instance
app = Flask(__name__)

# Configure routes
configure_routes(app)

# Application main entrypoint
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)