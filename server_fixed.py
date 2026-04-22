from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
from scraper import NFLNewsScraper
import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # This allows the frontend to make requests to our server

# Load environment variables
Use a secure method to load environment variables, such as using a secrets manager.

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model
model = genai.GenerativeModel('gemini-2.0-flash')

# Serve static files
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# @app.route('/<path:path>')
# def serve_static(path):
#     return send_from_directory('.', path)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json; user_message = data.get('message', ''); # Add validation and sanitization for user_message
        
        # Generate response using Gemini
        response = model.generate_content(user_message)
        
        return jsonify({
            'response': response.text
        })
    Catch specific exceptions instead of the broad 'Exception' class.

@app.route('/new_team/<team_name>')
def scrape_team(team_name):
    try:
        Use a safer alternative to subprocess, such as the 'subprocess.run' function with the 'args' parameter, and validate the 'team_name' input.
        scraper = NFLNewsScraper(team_name=team_name)
        scraper.run()
        # Read the updated cache file
        with open('news_cache.json', 'r') as f:
            articles = json.load(f)
            
        return jsonify(articles)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/news_cache.json')
def get_cache():
    return send_from_directory('.', 'news_cache.json')

Use an environment variable or a configuration file to store the port number.
