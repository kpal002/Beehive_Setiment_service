import os

def get_environment_variables():
    """
    Load and return environment variables for external services.
    
    Returns:
        dict: A dictionary containing the Watson API key, Watson URL, JWT secret key,
              Hugging Face API token, and Hugging Face model name.
    """
    return {
        "hf_token": os.getenv("HF_TOKEN"),  # Fetch the Hugging Face API token from environment variables
        "hf_model": os.getenv("HF_MODEL"),  # Fetch the Hugging Face model name from environment variables
        "jwt_secret_key": os.getenv("JWT_SECRET_KEY")
    }

