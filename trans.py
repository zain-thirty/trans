from flask import Flask, request, jsonify
import http.client
import urllib.parse
import json

app = Flask(__name__)

def extract_video_id(url):
    # Your existing logic to extract video ID from URL
    # Example: return url.split('v=')[1].split('&')[0]
    pass

def get_youtube_transcript(video_url):
    conn = http.client.HTTPSConnection("youtube-transcripts.p.rapidapi.com")
    
    headers = {
        'x-rapidapi-key': "c2e122140fmsh5a0be1dac9a5e0bp1aedb8jsnb98711b40c8d",
        'x-rapidapi-host': "youtube-transcripts.p.rapidapi.com"
    }
    
    # Encode the video URL for the API request
    encoded_url = urllib.parse.quote(video_url)
    request_url = f"/youtube/transcript?url={encoded_url}&chunkSize=500"
    
    conn.request("GET", request_url, headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    
    # Decode the response and parse it as JSON
    return json.loads(data.decode("utf-8"))

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
        # Fetch transcript using the new method
        transcript_json = get_youtube_transcript(url)

        if 'content' not in transcript_json:
            return jsonify({"error": "Transcript not found"}), 404

        # Combine all text segments into one string
        all_text = " ".join(segment['text'] for segment in transcript_json['content'])

        return jsonify({"transcript_text": all_text}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
