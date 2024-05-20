import requests
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report


def get_jwt_token():
    login_url = 'http://127.0.0.1:5000/login'
    credentials = {'username': 'admin', 'password': 'secret'}  # Adjust credentials as needed
    response = requests.post(login_url, json=credentials)
    
    if response.status_code == 200:
        token = response.json().get('access_token')
        return token
    else:
        print("Failed to get JWT token")
        print("Status Code:", response.status_code)
        print("Response Content:", response.text)
        return None


# Load your dataset
df = pd.read_csv('data/Tweets.csv')
df = df.head(3000)
# URL of your Flask endpoint
url = 'http://127.0.0.1:5000/sentiment'

# Obtain JWT token
jwt_token = get_jwt_token()

if not jwt_token:
    exit("Exiting due to failure in obtaining JWT.")

predictions = []
actuals = df['airline_sentiment'].tolist()  # Make sure this column name matches your data

# Headers with JWT
headers = {
    'Authorization': f'Bearer {jwt_token}',
    'Content-Type': 'application/json'
}


# Iterate over each row in the dataframe
for text in df['text']:
    payload = {'text': text}
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        try:
            response_data = response.json()
            # Extract the sentiment data safely
            sentiment_data = response_data.get('sentiment', {})
            predicted_label = sentiment_data.get('label', 'unknown')  # Default to 'unknown' if not found
            score = sentiment_data.get('score', 0.0)  # Default to 0.0 if not found
            sentiment_prob = sentiment_data.get('sentiment_prob')  # Retrieve sentiment probability
            
           
            predictions.append(predicted_label)
        except (KeyError, TypeError) as e:
            print(f"Error processing response data: {e}")
            predictions.append(None)  # Append None if there is an error processing data
    else:
        print("Failed to get a valid response, status code:", response.status_code)
        predictions.append(None)  # Append None if the request fails

# Calculate accuracy, ignoring None predictions
clean_predictions = [p for p in predictions if p is not None]
clean_actuals = [actuals[i] for i, p in enumerate(predictions) if p is not None]

# Calculate accuracy
accuracy = accuracy_score(clean_actuals, clean_predictions)
print(f"Accuracy: {accuracy:.2f}")

# Generate and print classification report
report = classification_report(clean_actuals, clean_predictions, target_names=['Negative', 'Neutral', 'Positive'])
print("Classification Report:\n", report)
