
from pathlib import Path
import tomllib

from google import genai

# Find the project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Read the API key without printing it
secrets_path = BASE_DIR / ".streamlit" / "secrets.toml"

with open(secrets_path, "rb") as file:
    secrets = tomllib.load(file)

api_key = secrets["GEMINI_API_KEY"]

# Connect to Gemini

from google.genai import types

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(
        timeout=20000,
        retry_options=types.HttpRetryOptions(
            attempts=1
        )
    )
)


from google.genai import errors

try:
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=(
            "Analyze this fictional financial headline: "
            "'A semiconductor company reports revenue "
            "above analyst expectations.' "
            "Classify the sentiment and explain the "
            "potential market implications in 3 sentences."
        ),
    )

    print("Gemini connection successful!")
    print(response.text)

except errors.ServerError as error:
    if error.code == 503:
        print(
            "Gemini is temporarily unavailable "
            "due to high demand."
        )
        print(
            "Your application is set up. "
            "Try the request again later."
        )
    else:
        print(f"Gemini server error: {error.code}")

except errors.ClientError as error:
    print(f"Gemini API request error: {error.code}")
    print(
        "Check your API key, selected model, "
        "and account permissions."
    )
