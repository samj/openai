#!/usr/bin/env python3
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import requests
import json
import os

# Set the API key for OpenAI
API_KEY = os.environ.get('OPENAI_API_KEY')

def pdf_to_text(file_path):
    """Convert a PDF to text using pdfminer"""
    text = ""
    with open(file_path, "rb") as f:
        rsrcmgr = PDFResourceManager()
        sio = StringIO()
        device = TextConverter(rsrcmgr, sio, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(f):
            interpreter.process_page(page)
            text += sio.getvalue()
        device.close()
        sio.close()
    return text

def summarize_text(text):
    """Summarize text using the OpenAI GPT-3 API"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    model = "text-davinci-002"
    prompt = {
        "prompt": f"summarize: {text}",
        "model": model,
        "max_tokens": 100
    }
    response = requests.post("https://api.openai.com/v1/models/{model}/jobs", headers=headers, json=prompt)

    if response.status_code == 200:
        response_json = response.json()
        return response_json["choices"][0]["text"]
    else:
        raise Exception(f"Error summarizing text: {response.text}")

if __name__ == "__main__":
    file_path = input("Enter the path to the PDF file: ")
    text = pdf_to_text(file_path)
    print(text)
    summary = summarize_text(text)
    print("Summary:")
    print(summary)
