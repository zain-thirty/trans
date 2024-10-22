import logging
from youtube_transcript_api import YouTubeTranscriptApi

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

def get_transcript_simple(url):
    # Function to extract video ID from URL
    def extract_video_id(url):
        try:
            # Simple video ID extraction assuming a standard YouTube URL format
            return url.split('v=')[1]
        except IndexError:
            return None

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
    url = "https://www.youtube.com/watch?v=Ma35a2h26Ec"
    result = get_transcript_simple(url)
    print(result)
