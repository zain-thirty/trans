import http.client
import urllib.parse
import json

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

# Example usage:
video_url = "https://youtu.be/Ma35a2h26Ec?si=o8ZOwJwkG"
transcript_json = get_youtube_transcript(video_url)
print(transcript_json)
