# YouTube Plugin

Fetch YouTube video transcripts and analyze them with Claude - summarize content, answer questions, or extract specific information.

## Setup

**Automatic**: Dependencies are installed automatically when the transcript skill is first invoked.

**Manual** (if needed):
```bash
cd /path/to/youtube
uv venv && uv pip install -r requirements.txt
```

## Usage

Use the `/youtube:transcript` skill followed by a video ID or URL and your request:

```
/youtube VIDEO_ID summarize this video
/youtube https://www.youtube.com/watch?v=VIDEO_ID what are the main points?
/youtube https://youtu.be/VIDEO_ID list all products mentioned
```

### Supported URL Formats

- Direct video ID: `dQw4w9WgXcQ`
- Standard URL: `https://www.youtube.com/watch?v=VIDEO_ID`
- Short URL: `https://youtu.be/VIDEO_ID`
- With parameters: `https://www.youtube.com/watch?v=VIDEO_ID&t=123`
- Shorts: `https://youtube.com/shorts/VIDEO_ID`
- Embed: `https://youtube.com/embed/VIDEO_ID`

### Example Requests

- "summarize this video"
- "what are the key takeaways?"
- "list all products reviewed"
- "what steps does the presenter recommend?"
- "who is mentioned in this video?"

## Limitations

- Some videos have transcripts disabled by the owner
- Auto-generated captions may contain minor transcription errors
- Very long videos may have lengthy transcripts

## Troubleshooting

**"youtube_transcript_api is not installed"**
Run the setup steps above to create the virtual environment and install dependencies.

**"No transcript available"**
The video doesn't have captions (manual or auto-generated).

**"Transcripts are disabled"**
The video owner has disabled transcript access.
