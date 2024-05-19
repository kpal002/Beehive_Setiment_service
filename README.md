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

