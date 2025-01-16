from flask import Flask, render_template, request, send_file
from langdetect import detect
from googletrans import Translator
from transformers import pipeline
import os

app = Flask(__name__)

# Sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.form["text"]

    # Language Detection
    detected_language = detect(text)

    # Translation to English (if not already English)
    translator = Translator()
    if detected_language != "en":
        translated_text = translator.translate(text, src=detected_language, dest="en").text
    else:
        translated_text = text

    # Sentiment Analysis
    sentiment = sentiment_pipeline(translated_text)[0]
    sentiment_label = sentiment["label"]
    sentiment_score = sentiment["score"]

    # Save results to file
    with open("analysis_results.txt", "w", encoding="utf-8") as file:
        file.write(f"Original Text: {text}\n")
        file.write(f"Detected Language: {detected_language}\n")
        file.write(f"Translated Text (if applicable): {translated_text}\n")
        file.write(f"Sentiment: {sentiment_label}\n")
        file.write(f"Confidence: {sentiment_score}\n")

    result = {
        "language": detected_language,
        "confidence": sentiment_score,
        "sentiment": sentiment_label,
    }
    return render_template("index.html", result=result)

@app.route("/download")
def download():
    # Send the analysis results file
    return send_file(
        "analysis_results.txt",
        as_attachment=True,
        download_name="analysis_results.txt",
    )

if __name__ == "__main__":
    app.run(debug=True)



