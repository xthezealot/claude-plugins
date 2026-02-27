---
name: transcript
description: Use when user asks to "fetch a YouTube transcript", "summarize a YouTube video", "get transcript from YouTube", "analyze a video", "what does this video say", or provides a YouTube URL or video ID for content extraction. Provides workflow for fetching, analyzing, and saving YouTube video transcripts.
---

# YouTube Transcript

Fetch YouTube video transcripts and analyze them based on user requests.

## Setup

Before fetching a transcript, run the setup script to ensure dependencies are installed:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/setup.sh"
```

This is a fast no-op if already set up (checks a marker file). Only run once per session.

## Fetching Transcripts

Run the Python script using the plugin's virtual environment:

```bash
"${CLAUDE_PLUGIN_ROOT}/.venv/bin/python" "${CLAUDE_PLUGIN_ROOT}/scripts/fetch_transcript.py" "<video_id_or_url>"
```

The script accepts YouTube video IDs (e.g., `dQw4w9WgXcQ`) and all standard URL formats (`youtube.com/watch?v=`, `youtu.be/`, shorts, embeds).

## Error Handling

Handle script errors as follows:

- "Transcripts are disabled" — Inform the user that the video owner has disabled transcripts
- "No transcript available" — Inform the user no transcript exists for this video
- "Video not found" — Inform the user the video ID or URL is invalid


## Analyzing Transcripts

After fetching, analyze the transcript based on the user's request:

- **Summarize**: Provide a concise summary of the video content
- **Answer questions**: Find relevant information in the transcript to answer
- **Extract information**: Pull out specific data (products, names, steps, etc.)
- **Other**: Fulfill whatever analysis the user requested

Identify and exclude in-video advertisements, sponsor segments, and commercial collaborations from the analysis. Do not include sponsored content in summaries or extracted information unless the user specifically asks about it.

Format responses clearly, citing relevant parts of the transcript when appropriate.

## Content Saving Rules

When saving or summarizing content (transcripts, conversations, threads):

- Always save the COMPLETE content unless explicitly told to summarize
- Never claim content is stored somewhere it isn't
- If saving highlights, clearly label them as highlights and ask if the full content should also be saved

## Notes

- The script automatically selects the best available transcript language
- Supports various YouTube URL formats (youtube.com, youtu.be, shorts, embeds)
- Transcripts may include auto-generated captions which can have minor errors
