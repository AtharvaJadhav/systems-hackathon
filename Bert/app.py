# app.py

from flask import Flask, render_template, request, jsonify
from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn import functional as F
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import torch
import requests
import openai

app = Flask(__name__)

# Rate limiter setup
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Initialize BERT classifier
MODEL_NAME = "./trained_model"
TOKENIZER = BertTokenizer.from_pretrained(MODEL_NAME)
MODEL = BertForSequenceClassification.from_pretrained(MODEL_NAME)
MODEL.eval()

# OpenAI API constants
openai.api_key = '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'
# API_ENDPOINT = "https://api.openai.com/v2/engines/davinci/completions"
# HEADERS = {
#     "Authorization": "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"
# }

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/ask', methods=["POST"])
@limiter.limit("5 per minute")
def ask_question():
    question = request.form.get("question")
    
    # Check if question is tax-related using the BERT model
    inputs = TOKENIZER(question, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = MODEL(**inputs)
        probs = F.softmax(outputs.logits, dim=-1)
        label = torch.argmax(probs, dim=-1).item()

    # If the question is not related to tax
    if label == 0:
        return jsonify({"response": "This question doesn't seem related to tax. Please reenter your question."})
    else:
        # If the question is related to tax, get a detailed response from OpenAI API
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"US Tax Law about {question}:",
            max_tokens=150
        )
        gpt_response = response.choices[0].text.strip()
        return jsonify({"response": gpt_response})

@app.errorhandler(429)
def ratelimit_error(e):
    return jsonify(error="ratelimit exceeded", message=str(e.description)), 429

if __name__ == "__main__":
    app.run(debug=True)
