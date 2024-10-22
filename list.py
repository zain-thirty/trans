from flask import Flask, request, jsonify
from flask_cors import CORS
import http.client
import urllib.parse
import json

app = Flask(__name__)
CORS(app)  # Enable CORS to allow cross-origin requests

def get_youtube_transcript(video_url):
    conn = http.client.HTTPSConnection("youtube-transcripts.p.rapidapi.com")
    
    headers = {
        'x-rapidapi-key': "c2e122140fmsh5a0be1dac9a5e0bp1aedb8jsnb98711b40c8d",
        'x-rapidapi-host': "youtube-transcripts.p.rapidapi.com"
    }
    
    # Encode the video URL for the API request
    encoded_url = urllib.parse.quote(video_url)
    request_url = f"/youtube/transcript?url={encoded_url}"
    
    conn.request("GET", request_url, headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    
    # Decode the response and parse it as JSON
    transcript_json = json.loads(data.decode("utf-8"))
    
    # Extract all text from the transcript segments
    all_text = ""
    if 'content' in transcript_json:
        for segment in transcript_json['content']:
            all_text += segment['text'] + " "  # Add each segment text with a space
    
    # Return the concatenated transcript text as well
    return {
        
        "all_text": all_text.strip()  # Remove trailing spaces
    }

# Define an endpoint to retrieve transcript
@app.route('/transcript', methods=['POST'])
def transcript():
    try:
        # Get the video URL from the JSON request body
        req_data = request.get_json()
        video_url = req_data.get('video_url')
        
        if not video_url:
            return jsonify({"error": "No video URL provided"}), 400
        
        # Get transcript for the given video URL
        transcript_data = get_youtube_transcript(video_url)
        return jsonify(transcript_data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
