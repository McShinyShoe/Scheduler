from flask import Flask
from routes import configure_routes  # Import the function to configure routes

app = Flask(__name__)

# Configure routes by passing the app instance
configure_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)