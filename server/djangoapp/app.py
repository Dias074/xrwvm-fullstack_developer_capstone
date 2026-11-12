from pathlib import Path
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from flask import Flask, jsonify
nltk.data.path.insert(0,str(Path(__file__).parent))
app=Flask(__name__)
analyzer=SentimentIntensityAnalyzer()
@app.get('/')
def health():
    return jsonify(status='ok',service='sentiment')
@app.get('/analyze/<path:text>')
def analyze(text):
    score=analyzer.polarity_scores(text)['compound']
    return jsonify(sentiment='positive' if score>=0.05 else 'negative' if score<=-0.05 else 'neutral',compound=score)
if __name__=='__main__':
    app.run(host='0.0.0.0',port=5050)
