---
name: youtube
description: Fetch YouTube video transcript and analyze content (summarize, answer questions, extract information)
argument-hint: <video_id_or_url> <your request, e.g., "summarize" or a question>
allowed-tools:
  - Bash
---

# YouTube Transcript Analyzer

Fetch a YouTube video's transcript and analyze it based on the user's request.

## Instructions

1. **Parse user input**: The user provides a video ID or URL, followed by their analysis request (summarize, answer a question, extract information, etc.)

2. **Fetch the transcript**: Run the Python script using the plugin's virtual environment:
   ```bash
   "${CLAUDE_PLUGIN_ROOT}/.venv/bin/python" "${CLAUDE_PLUGIN_ROOT}/scripts/fetch_transcript.py" "<video_id_or_url>"
   ```

3. **Handle errors**: If the script returns an error:
   - "Transcripts are disabled" - Inform user the video owner has disabled transcripts
   - "No transcript available" - Inform user no transcript exists for this video
   - "Video not found" - Inform user the video ID/URL is invalid
   - "youtube_transcript_api is not installed" - Tell user to run: `pip install youtube-transcript-api`

4. **Analyze the transcript**: Based on the user's request:
   - **Summarize**: Provide a concise summary of the video content
   - **Answer questions**: Find relevant information in the transcript to answer
   - **Extract information**: Pull out specific data (products, names, steps, etc.)
   - **Other**: Fulfill whatever analysis the user requested

5. **Present findings**: Format your response clearly, citing relevant parts of the transcript when appropriate.

## Examples

User: `dQw4w9WgXcQ summarize this video`
Action: Fetch transcript for dQw4w9WgXcQ, then provide a summary

User: `https://www.youtube.com/watch?v=VIDEO_ID what are the main takeaways?`
Action: Fetch transcript from URL, then list main takeaways

User: `https://youtu.be/VIDEO_ID list all products mentioned`
Action: Fetch transcript, then extract and list product names

## Notes

- The script automatically selects the best available transcript language
- Supports various YouTube URL formats (youtube.com, youtu.be, shorts, embeds)
- Transcripts may include auto-generated captions which can have minor errors
