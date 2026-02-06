#!/usr/bin/env python3
"""Fetch YouTube video transcript using youtube_transcript_api."""

import sys
import re
from urllib.parse import urlparse, parse_qs

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import (
        TranscriptsDisabled,
        NoTranscriptFound,
        VideoUnavailable,
    )
except ImportError:
    print("Error: youtube_transcript_api is not installed.")
    print("Install it with: pip install youtube-transcript-api")
    sys.exit(1)


def extract_video_id(input_str: str) -> str | None:
    """Extract video ID from URL or return input if already an ID."""
    input_str = input_str.strip()

    # Check if it's already a video ID (11 characters, alphanumeric with - and _)
    if re.match(r'^[a-zA-Z0-9_-]{11}$', input_str):
        return input_str

    # Try to parse as URL
    try:
        parsed = urlparse(input_str)

        # Handle youtu.be short URLs
        if parsed.netloc in ('youtu.be', 'www.youtu.be'):
            video_id = parsed.path.lstrip('/')
            if video_id:
                return video_id.split('/')[0]

        # Handle youtube.com URLs
        if parsed.netloc in ('youtube.com', 'www.youtube.com', 'm.youtube.com'):
            # Standard watch URL: youtube.com/watch?v=VIDEO_ID
            if parsed.path == '/watch':
                query_params = parse_qs(parsed.query)
                if 'v' in query_params:
                    return query_params['v'][0]

            # Shortened URL: youtube.com/v/VIDEO_ID
            if parsed.path.startswith('/v/'):
                return parsed.path[3:].split('/')[0]

            # Embed URL: youtube.com/embed/VIDEO_ID
            if parsed.path.startswith('/embed/'):
                return parsed.path[7:].split('/')[0]

            # Shorts URL: youtube.com/shorts/VIDEO_ID
            if parsed.path.startswith('/shorts/'):
                return parsed.path[8:].split('/')[0]
    except Exception:
        pass

    return None


def fetch_transcript(video_id: str) -> str:
    """Fetch transcript for a video and return as plain text."""
    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)

    # Try to get manually created transcript first, then auto-generated
    transcript = None
    try:
        # Try manual transcripts in common languages
        transcript = transcript_list.find_manually_created_transcript(
            ['en', 'en-US', 'en-GB', 'es', 'fr', 'de', 'pt', 'it', 'ja', 'ko', 'zh']
        )
    except NoTranscriptFound:
        try:
            # Fall back to auto-generated
            transcript = transcript_list.find_generated_transcript(
                ['en', 'en-US', 'en-GB', 'es', 'fr', 'de', 'pt', 'it', 'ja', 'ko', 'zh']
            )
        except NoTranscriptFound:
            # Last resort: get any available transcript
            for t in transcript_list:
                transcript = t
                break
            if transcript is None:
                raise NoTranscriptFound(video_id, [], None)

    # Fetch the transcript data
    transcript_data = transcript.fetch()

    # Combine all text segments
    full_text = ' '.join(snippet.text for snippet in transcript_data)

    return full_text


def main():
    if len(sys.argv) < 2:
        print("Usage: fetch_transcript.py <video_id_or_url>")
        print("Examples:")
        print("  fetch_transcript.py dQw4w9WgXcQ")
        print("  fetch_transcript.py https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        print("  fetch_transcript.py https://youtu.be/dQw4w9WgXcQ")
        sys.exit(1)

    input_str = sys.argv[1]
    video_id = extract_video_id(input_str)

    if not video_id:
        print(f"Error: Could not extract video ID from: {input_str}")
        sys.exit(1)

    try:
        transcript = fetch_transcript(video_id)
        print(transcript)
    except TranscriptsDisabled:
        print(f"Error: Transcripts are disabled for video: {video_id}")
        sys.exit(1)
    except NoTranscriptFound:
        print(f"Error: No transcript available for video: {video_id}")
        sys.exit(1)
    except VideoUnavailable:
        print(f"Error: Video not found or unavailable: {video_id}")
        sys.exit(1)
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
