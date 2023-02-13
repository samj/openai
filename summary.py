#!/usr/bin/env python3
import os
import PyPDF2
import requests
import json

# Set the API key for OpenAI
API_KEY = os.environ.get('OPENAI_API_KEY')

def pdf_to_text(file_path):
    """Convert a PDF to text using PyPDF2"""
    with open(file_path, "rb") as f:
        pdf = PyPDF2.PdfFileReader(f)
        text = " ".join([pdf.getPage(page_num).extractText() for page_num in range(pdf.numPages)])
    return text

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
