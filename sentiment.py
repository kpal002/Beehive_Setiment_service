import logging
import requests
from flask import jsonify
from transformers import pipeline
from config import get_environment_variables


def initialize_huggingface_nlu():
    """
    Initializes and configures the Hugging Face API connection.

    Retrieves the API token and model information from environment variables, constructs the API URL,
    and prepares the authorization headers required for making API calls.

    Returns:
        tuple: Contains the API URL (str) and headers (dict) configured for authorization.

    Raises:
        Exception: If there is a failure in retrieving environment variables or if any configuration
                   setting is missing, an exception is logged and re-raised to indicate initialization failure.
    """
    try:
        env_vars = get_environment_variables()
        hf_token = env_vars['hf_token']
        model = env_vars.get('hf_model', 'cardiffnlp/twitter-roberta-base-sentiment-latest')
        api_url = f"https://api-inference.huggingface.co/models/{model}"
        headers = {"Authorization": f"Bearer {hf_token}"}
        logging.info("Hugging Face API initialized successfully.")
        return api_url, headers
    except Exception as e:
        logging.error(f"Failed to initialize Hugging Face API: {e}", exc_info=True)
        raise

def get_transformer_model():
    """
    Loads and returns a pre-trained sentiment analysis model from Hugging Face's Transformers.

    This function specifically loads a Roberta model pre-trained for sentiment analysis tasks.
    
    Returns:
        pipeline: A Hugging Face pipeline object configured for sentiment analysis.

    Raises:
        Exception: If the model fails to load, logs the error and re-raises an exception.
    """
    try:
        model_path = 'cardiffnlp/twitter-roberta-base-sentiment-latest'
        model = pipeline('sentiment-analysis', model=model_path)
        logging.info("Local Transformer model loaded successfully.")
        return model
    except Exception as e:
        logging.error(f"Failed to load Transformer model: {e}", exc_info=True)
        raise

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text using the Hugging Face API with a fallback to a local model.

    This function attempts to analyze sentiment via an external API and falls back to a locally hosted model
    if the API is unavailable.

    Args:
        text (str): The text for which sentiment analysis is to be performed.

    Returns:
        dict: A dictionary containing the sentiment label, its score, and a numeric sentiment value.

    Raises:
        Exception: If both Hugging Face API and local model fail, it logs the error and returns
                   an internal server error response.
    """
    try:
        api_url, headers = initialize_huggingface_nlu()
        payload = {"inputs": text, "options": {"wait_for_model": True}}
        response = requests.post(api_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            response_data = response.json()
            if response_data:
                # Process API response data as needed
                # Assuming response_data[0] is where the relevant data resides
                sentiment_data = response_data[0]
                max_score = -1
                dominant_sentiment = 'unknown'
                for sentiment_dict in sentiment_data:
                    if sentiment_dict['score'] > max_score:
                        max_score = sentiment_dict['score']
                        dominant_sentiment = sentiment_dict['label']
                label_to_numeric = {'negative': -1, 'neutral': 0, 'positive': 1}
                numeric_sentiment = label_to_numeric.get(dominant_sentiment.lower(), 0) * max_score
                return {
                    'label': dominant_sentiment,
                    'score': max_score,
                    'numeric_sentiment': numeric_sentiment
                }
            else:
                raise ValueError("Empty response from API.")
        else:
            raise ValueError("Failed to get valid response from API. Status code: {}".format(response.status_code))
    except (requests.exceptions.RequestException, ValueError) as e:
        logging.error("Error with Hugging Face API or invalid response: {}. Falling back to local model.".format(e))
        # Fall back to local model on network error or bad response
        model = get_transformer_model()
        result = model(text)[0]
        label_to_numeric = {'POSITIVE': 1, 'NEGATIVE': -1, 'NEUTRAL': 0}
        numeric_sentiment = label_to_numeric.get(result['label'].upper(), 0) * result['score']
        return {
            'label': result['label'],
            'score': result['score'],
            'numeric_sentiment': numeric_sentiment
        }



