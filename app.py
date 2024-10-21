from flask import Flask, jsonify, request
from langchain_community.document_loaders import YoutubeLoader
import json

app = Flask(__name__)

@app.route('/transcript', methods=['POST'])
def get_transcript():
    # Get the JSON payload from the request body
    request_data = request.get_json()
    
    if not request_data or 'url' not in request_data:
        return jsonify({'error': 'You must provide a YouTube URL in the request body'}), 400
    
    youtube_url = request_data['url']
    
    try:
        # Load the YouTube transcript
        loader = YoutubeLoader.from_youtube_url(youtube_url, add_video_info=False)
        documents = loader.load()

        # Convert the documents to a JSON format
        data = []
        for doc in documents:
            data.append({
                'transcript': doc.page_content,
            })

        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
