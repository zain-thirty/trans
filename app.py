from flask import Flask, jsonify, request
from langchain_community.document_loaders import YoutubeLoader
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 


@app.route('/get_transcript', methods=['POST'])
def get_transcript():
    # data = request.json
    # url = data.get('url')

    # if not url:
    #     return jsonify({"error": "URL is required"}), 400

    # video_id = extract_video_id(url)

    # if not video_id:
    #     return jsonify({"error": "Invalid YouTube URL"}), 400

    try:
        # Fetch transcript
        transcript = YouTubeTranscriptApi.get_transcript("Ma35a2h26Ec", languages=['en'])
        print(transcript)
        transcript_text = " ".join([t['text'] for t in transcript])

        return jsonify({"transcript_text": transcript_text}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
