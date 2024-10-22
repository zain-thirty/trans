import logging
from youtube_transcript_api import YouTubeTranscriptApi
import re

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Function to extract video ID from URL
def extract_video_id(url):
    patterns = [
        r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtube\.com/embed/|youtu.be/)([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

# Function to fetch transcript from video ID
def fetch_transcript(url):
    if not url:
        logging.error("URL is missing")
        return {"error": "URL is required"}

    video_id = extract_video_id(url)

    if not video_id:
        logging.error("Invalid YouTube URL provided")
        return {"error": "Invalid YouTube URL"}

    try:
        # Fetch transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        logging.debug(f"Transcript fetched: {transcript}")

        # Join all transcript text
        transcript_text = " ".join([t['text'] for t in transcript])

        return {"transcript_text": transcript_text}

    except Exception as e:
        logging.error(f"Error occurred while fetching transcript: {str(e)}")
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    # Provide a YouTube URL to test
    url = "http://youtu.be/Ma35a2h26Ec?si=o8ZOwJwkG"
    result = fetch_transcript(url)
    print(result)
