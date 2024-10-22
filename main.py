import os
import requests
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled

app = Flask(__name__)

# Add your proxy settings here (example for HTTP and HTTPS)
proxies = {
    "http": os.getenv('HTTP_PROXY', ''),
    "https": os.getenv('HTTPS_PROXY', '')
}

@app.route('/get_transcript', methods=['POST'])
def get_transcript():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "URL is required"}), 400

    video_id = extract_video_id(url)

    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    try:
        # Fetch transcript using proxies (if necessary)
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'], proxies=proxies)
        print(transcript)
        transcript_text = " ".join([t['text'] for t in transcript])

        return jsonify({"transcript_text": transcript_text}), 200

    except TranscriptsDisabled:
        return jsonify({"error": "Transcripts are disabled for this video."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
