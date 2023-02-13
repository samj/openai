#!/usr/bin/env python3

import argparse
import openai
import os
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

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
    model = "text-davinci-002"
    prompt = f"summarize: {text}"
    completions = openai.Completion.create(engine=model, prompt=prompt, max_tokens=500, n=1, stop=None, temperature=0.5)
    message = completions.choices[0].text
    return message

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="The path to the PDF file")
    args = parser.parse_args()
    file_path = args.file_path

    # Set the API key for OpenAI
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key is None:
        raise Exception("The OPENAI_API_KEY environment variable is not set")
    openai.api_key = api_key

    text = pdf_to_text(file_path)
    summary = summarize_text(text)
    print("Summary:")
    print(summary)
