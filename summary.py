import requests
import json

# Set the API key for OpenAI
API_KEY = "your_api_key_here"

def pdf_to_text(file_path):
    """Convert a PDF to text using the OpenAI GPT-3 API"""
    headers = {
        "Content-Type": "application/pdf",
        "Authorization": f"Bearer {API_KEY}"
    }
    with open(file_path, "rb") as f:
        response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, data=f)

    if response.status_code == 200:
        response_json = response.json()
        return response_json["data"][0]["text"]
    else:
        raise Exception(f"Error converting PDF to text: {response.text}")

def summarize_text(text):
    """Summarize text using the OpenAI GPT-3 API"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    model = "text-davinci-002"
    prompt = (f"summarize: {text}"
              f"model: {model}"
              f"max_tokens: 100")
    response = requests.post("https://api.openai.com/v1/engines/{model}/jobs", headers=headers, data=prompt)

    if response.status_code == 200:
        response_json = response.json()
        return response_json["choices"][0]["text"]
    else:
        raise Exception(f"Error summarizing text: {response.text}")

if __name__ == "__main__":
    file_path = input("Enter the path to the PDF file: ")
    text = pdf_to_text(file_path)
    summary = summarize_text(text)
    print("Summary:")
    print(summary)
