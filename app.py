import logging
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from transformers import pipeline
from sentiment import analyze_sentiment  # Adjusted for Hugging Face
from config import get_environment_variables
from datetime import timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, filename='flask_app.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.logger.setLevel(logging.INFO)  # Set logging level to INFO

# Load environment variables
env_vars = get_environment_variables()
expires = timedelta(minutes=60)
app.config['JWT_SECRET_KEY'] = env_vars['jwt_secret_key']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = expires

# Initialize JWT Manager
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    """
    Authenticate a user and return a JWT.

    Expects JSON with 'username' and 'password'.
    Returns a JSON web token for valid credentials.
    """
    
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username == 'admin' and password == 'secret':  # Example hardcoded credentials
        access_token = create_access_token(identity=username, expires_delta=expires)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401


@app.route('/')
def home():
    """
    Home endpoint to check the service's availability.

    Returns a simple welcome string.
    """
    return "Welcome to the Sentiment Analysis Service!"

@app.route('/sentiment', methods=['POST'])
@jwt_required()
def sentiment():
    """
    Perform sentiment analysis on provided text data.

    Requires JWT authentication.
    Expects a JSON payload with a 'text' key.
    Returns the sentiment score as a JSON object.
    """
    current_user = get_jwt_identity()
    app.logger.info(f"Request made by user: {current_user}")

    if not request.is_json:
        return jsonify({"error": "Invalid input, JSON expected"}), 400

    text = request.json.get('text', '')
    if not text:
        return jsonify({"error": "Text is required for sentiment analysis"}), 400

    try:
        sentiment_score = analyze_sentiment(text)
        return jsonify({"sentiment": sentiment_score}), 200
    except Exception as e:
        logging.error(f"Unhandled exception during sentiment analysis: {e}")
        return jsonify({"error": "Internal server error"}), 500


# Custom error handlers for better error control
@app.errorhandler(404)
def resource_not_found(e):
    """
    Custom error handler for 404 Not Found.
    """
    return jsonify(error=str(e)), 404

@app.errorhandler(Exception)
def handle_exception(e):
    """
    Generic error handler for any unhandled exceptions.
    """
    # Pass through HTTP errors
    if isinstance(e, HTTPException):
        return e
    # Non-HTTP exceptions
    return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

