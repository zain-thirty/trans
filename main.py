from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id="Ma35a2h26Ec", language='en'):
    try:
        # Fetch transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        transcript_text = " ".join([t['text'] for t in transcript])
        
        return {"transcript_text": transcript_text}

    except Exception as e:
        return {"error": str(e)}

# Example call to the function
result = get_transcript()
print(result)
