from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import json
import os

app = Flask(__name__)
CORS(app)  # This allows the frontend to make requests to our server

@app.route('/new_team/<team_name>')
def scrape_team(team_name):
    try:
        # Run the scraper script with the team ID as an argument
        subprocess.run(['python', '../scraper.py', team_name], check=True)
        
        # Read the updated cache file
        with open('news_cache.json', 'r') as f:
            articles = json.load(f)
            
        return jsonify(articles)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/news_cache.json')
def get_cache():
    return send_from_directory('../', 'news_cache.json')

if __name__ == '__main__':
    app.run(debug=True, port=5000) 