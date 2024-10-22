import logging
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import os
from youtube_transcript_api._errors import CouldNotRetrieveTranscript

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Test connection to YouTube
def test_youtube_access(proxies=None):
    test_url = 'https://www.youtube.com'
    try:
        response = requests.get(test_url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            logging.info("Successfully accessed YouTube")
        else:
            logging.error(f"Failed to access YouTube: {response.status_code}")
    except requests.RequestException as e:
        logging.error(f"Network/Proxy error: {e}")
        return False
    return True

# Fetch transcript with proxy handling
def fetch_transcript_with_proxy(video_id):
    proxies = {
        'http': os.getenv('HTTP_PROXY', ''),  # Set your HTTP proxy here
        'https': os.getenv('HTTPS_PROXY', '')  # Set your HTTPS proxy here
    }

    # Test proxy or direct connection
    if not test_youtube_access(proxies):
        return {"error": "Failed to connect to YouTube, check your proxy or network settings."}

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies=proxies)
        logging.debug(f"Transcript fetched: {transcript}")
        transcript_text = " ".join([t['text'] for t in transcript])
        return {"transcript_text": transcript_text}
    except CouldNotRetrieveTranscript as e:
        logging.error(f"Could not retrieve transcript: {str(e)}")
        return {"error": "Could not retrieve transcript. Subtitles may be disabled."}
    except Exception as e:
        logging.error(f"General error occurred: {str(e)}")
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    video_id = 'Ma35a2h26Ec'  # Example video ID
    result = fetch_transcript_with_proxy(video_id)
    print(result)
