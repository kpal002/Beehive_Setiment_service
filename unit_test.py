import unittest
from flask import json
from app import app  # Import the Flask app

class FlaskAppTests(unittest.TestCase):
    """
    Test suite for the Flask sentiment analysis application.
    """
    
    def setUp(self):
        """
        Prepare the app for testing.
        Sets the app to testing mode, which affects error catching and other behaviors.
        It also configures a test-specific secret key.
        """
        app.config['TESTING'] = True
        app.config['JWT_SECRET_KEY'] = 'test_secret_key'
        self.app = app.test_client()

    def test_home(self):
        """
        Test the home endpoint to ensure it is reachable and returns the correct welcome message.
        """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to the Sentiment Analysis Service!', response.data.decode('utf-8'))

    def test_login(self):
        """
        Test the login functionality to ensure it responds correctly to valid credentials
        and returns a JWT token.
        """
        response = self.app.post('/login', json={'username': 'admin', 'password': 'secret'})
        self.assertEqual(response.status_code, 200)
        # Check if a token is returned in the response
        self.assertIn('access_token', json.loads(response.data))

    def test_sentiment_authenticated(self):
        """
        Test the sentiment analysis endpoint with valid authentication.
        This test ensures that the endpoint correctly processes authenticated requests.
        """
        # Obtain a token for testing
        login_response = self.app.post('/login', json={'username': 'admin', 'password': 'secret'})
        access_token = json.loads(login_response.data)['access_token']

        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = self.app.post('/sentiment', headers=headers, json={'text': 'I love flying!'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('sentiment', json.loads(response.data))

    def test_sentiment_unauthenticated(self):
        """
        Ensure that unauthenticated requests to the sentiment endpoint are properly blocked.
        This test checks for the correct handling of unauthorized access.
        """
        response = self.app.post('/sentiment', json={'text': 'I love flying!'})
        self.assertEqual(response.status_code, 401)  # 401 Unauthorized

if __name__ == '__main__':
    unittest.main()

