# Sentiment Analysis Service

This repository contains a Python-based Flask application designed to perform sentiment analysis on text data, specifically tweets from the Twitter US Airline Sentiment dataset. The service utilizes both an external API and a local language model to analyze sentiment, defaulting to the external API with a fallback to the local model if the API is unavailable.

## Project Objective

The goal of this project is to develop a robust sentiment analysis service that can accurately and at scale detect sentiment in text data, providing a numeric sentiment value ranging from -1 to 1. The service is protected with Bearer authentication and follows best practices in software development to ensure clean, modular, and maintainable code.

## Features

- **HTTP POST Endpoint**: Exposes a `/sentiment` endpoint that accepts text as input and returns a numeric sentiment value.
- **Dual Analysis Methods**: Uses an external API by default for sentiment analysis with a fallback to a local model if needed.
- **Bearer Authentication**: Protects the service using token-based authentication.
- **Error Handling**: Includes comprehensive server-side logging and user-friendly error messages.

## Requirements

- Python 3.8+
- Flask
- Requests
- Transformers (Hugging Face)
- Any other dependencies listed in `requirements.txt`

## Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-github-username/sentiment-analysis-service.git
   cd sentiment-analysis-service

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a .env file in the project root and add the following variables:

```
HF_TOKEN=your_huggingface_api_token
HF_MODEL=optional_model_identifier
JWT_SECRET_KEY=your_jwt_secret_key
```

## What is a JWT Secret Key?
A JWT (JSON Web Token) secret key is a crucial component used to sign and verify the tokens to ensure their integrity and security. JSON Web Tokens are an open standard used primarily for securely transmitting information between parties as a compact JSON object. This information can be verified and trusted because it is digitally signed using a secret key or a public/private key pair.

Purpose of the JWT Secret Key
The JWT secret key is used in the signing process to create the signature part of the JWT. The signature ensures that the token hasn’t been altered after it was issued and is also used to verify that the sender of the JWT is who it says it is and to ensure that the message wasn't changed along the way.

Here’s how it works:

- Signing: When a JWT is created, its header, payload, and secret key are taken, and an algorithm (specified in the header) is applied to produce a unique signature. If the JWT includes sensitive information, it can also be encrypted.

-Verification: When a JWT is received, the signature is verified using the secret key. If the signature is valid, it confirms the token’s integrity, that the sender of the JWT possesses the secret key, and that the token was not tampered with.

### How to Generate a JWT Secret Key
The security of your JWT implementation depends significantly on the secret key. It should be:

- Sufficiently Random: Unpredictable and not easily guessable.
- Secret: Only accessible to parties responsible for issuing and validating tokens.
- Unique: Preferably different for each environment or application.

Here are some methods to generate a secure JWT secret key:

- Using a Command Line Tool

1. On Linux or macOS, you can use:
```bash
openssl rand -base64 32
```

2. On Windows, using PowerShell:
```
[System.Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes(32))
```

3. Using a Programming Language

Python example:

```bash
import os
import base64
secret_key = base64.urlsafe_b64encode(os.urandom(32))
print(secret_key.decode())
```

Node.js example:

```bash
require('crypto').randomBytes(32, function(err, buffer) {
  var token = buffer.toString('base64');
  console.log(token);
});
```

## Run the application

```bash
python app.py
```

## Authentication

Before sending requests to the `/sentiment` endpoint, you need to authenticate and obtain a JWT token. Here is how you can log in to retrieve the token:

```bash
curl -X POST http://127.0.0.1:5000/login \
     -H 'Content-Type: application/json' \
     -d '{"username": "admin", "password": "secret"}'
```

This will return a JWT token which you should include in the Authorization header of subsequent requests.

## Sending a Request
Once authenticated, you can send a POST request to the /sentiment endpoint with a JSON payload containing the text to analyze. Use the JWT token received from the login step in the Authorization header:

```bash
curl -X POST http://127.0.0.1:5000/sentiment \
     -H 'Authorization: Bearer YourJWTTokenHere' \
     -H 'Content-Type: application/json' \
     -d '{"text": "I love flying!"}'
```


### Key Points to Include:

- **Security Warning**: The credentials used in the examples are for testing and demonstration purposes and should not be used in a production environment.
- **Authentication Best Practices**: There should be a secure method for authenticating users, such as verifying credentials against a database or using an OAuth provider.

These updates ensure users understand the importance of proper authentication practices and encourage them to implement secure methods in their deployments. This approach not only protects the application but also educates users on maintaining the security and integrity of their interactions with the service.

## Testing

### Unit Tests

Unit tests for the application are located in the `unit_tests.py` file. These tests cover critical components of the application, ensuring that both the external API and the fallback local model function correctly under various scenarios. To run these tests, use the following command:

```bash
python -m unittest unit_test
```

## Script for Analyzing Tweets

The tweets.py script is designed to analyze tweets using the sentiment analysis service. It processes tweets from the Twitter US Airline Sentiment dataset and sends them to the /sentiment endpoint. This script is useful for batch processing or testing the service with real data. The dataset can be found inside the Data Folder.

## Output 
```
{
  "sentiment": {
    "label": "neutral",
    "numeric_sentiment": 0.0,
    "score": 0.8863000273704529
  }
}
```

**Fields:**

- label: This field indicates the categorical sentiment classification based on the analyzed text. In this case, the label is "neutral", which suggests that the sentiment expressed in the text does not have a strongly positive or negative emotional charge. Other possible values might include "positive" or "negative" depending on the sentiment analysis model's capabilities and configuration.

- numeric_sentiment: This field provides a numeric representation of the sentiment where the range typically is between -1 and 1. A value of 0.0 in this context confirms that the sentiment is neutral. The range generally interprets as:

-1: Strongly negative
0: Neutral
1: Strongly positive

This numeric scale helps in quantifying sentiment in a way that can be easily aggregated or compared across different texts or data points.

- score: This value, which is 0.8863000273704529 in the output, represents the confidence score of the sentiment analysis model regarding the assigned label. The score is a floating-point number between 0 and 1, where a higher score indicates greater confidence in the sentiment classification. In this case, a score of approximately 0.886 suggests that the model is quite confident in its classification of the sentiment as neutral.
