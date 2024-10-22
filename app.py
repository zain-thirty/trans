import logging
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._api import TranscriptApiException
import re
import os
import requests

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

# Function to fetch transcript using a proxy
def fetch_transcript(url):
    if not url:
        logging.error("URL is missing")
        return {"error": "URL is required"}

    video_id = extract_video_id(url)

    if not video_id:
        logging.error("Invalid YouTube URL provided")
        return {"error": "Invalid YouTube URL"}

    try:
        # Set up proxies (adjust as needed)
        proxies = {
            "http": os.getenv("HTTP_PROXY", ""),  # Add your HTTP proxy here if necessary
            "https": os.getenv("HTTPS_PROXY", "")  # Add your HTTPS proxy here if necessary
        }
        
        # Test the proxy connection before making the API request
        test_url = "http://google.com"
        try:
            requests.get(test_url, proxies=proxies, timeout=5)
            logging.info("Proxy connection successful")
        except requests.RequestException as e:
            logging.error(f"Failed to connect via proxy: {e}")
            return {"error": f"Proxy connection failed: {e}"}
        
        # Fetch transcript through the proxy
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'], proxies=proxies)
        logging.debug(f"Transcript fetched: {transcript}")

        # Join all transcript text
        transcript_text = " ".join([t['text'] for t in transcript])

        return {"transcript_text": transcript_text}

    except TranscriptApiException as e:
        logging.error(f"Error occurred while fetching transcript: {str(e)}")
        return {"error": str(e)} 
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    # Provide a YouTube URL to test
    url = "http://youtu.be/Ma35a2h26Ec?si=o8ZOwJwkG"
    result = fetch_transcript(url)
    print(result)
