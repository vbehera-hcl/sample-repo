# n8n Voice AI Agent

A complete voice-to-voice AI agent workflow for n8n that processes voice input, generates intelligent responses using GPT-4, and returns audio responses.

## Features

- **Speech-to-Text**: Converts audio input to text using OpenAI Whisper
- **AI Processing**: Uses GPT-4o for intelligent, conversational responses
- **Text-to-Speech**: Converts AI responses back to natural speech
- **Conversation Memory**: Maintains context across multiple interactions
- **Built-in Tools**: Calculator, web search, and current time functions
- **Input Validation**: Validates audio input and returns helpful error messages

## Workflow Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Voice Input    │────▶│  Validate Audio  │────▶│  Speech to Text │
│  (Webhook)      │     │  Input           │     │  (Whisper)      │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                │                         │
                                ▼                         ▼
                        ┌──────────────────┐     ┌─────────────────┐
                        │  Error Response  │     │  AI Agent       │
                        │  (400)           │     │  (GPT-4o)       │
                        └──────────────────┘     └─────────────────┘
                                                          │
                              ┌────────────────┬──────────┴──────────┐
                              ▼                ▼                     ▼
                        ┌──────────┐    ┌────────────┐    ┌─────────────────┐
                        │ Memory   │    │ LLM Model  │    │ Tools           │
                        │ Buffer   │    │ (GPT-4o)   │    │ (Time/Search/   │
                        └──────────┘    └────────────┘    │  Calculator)    │
                                                          └─────────────────┘
                                                          │
                                                          ▼
                                                 ┌─────────────────┐
                                                 │  Text to Speech │
                                                 │  (TTS)          │
                                                 └─────────────────┘
                                                          │
                                                          ▼
                                                 ┌─────────────────┐
                                                 │  Send Voice     │
                                                 │  Response       │
                                                 └─────────────────┘
```

## Prerequisites

1. **n8n Instance** (v1.0+ recommended)
2. **OpenAI API Key** - For Whisper (STT), GPT-4 (AI), and TTS
3. **Tavily API Key** (Optional) - For web search functionality

## Installation

### Step 1: Import the Workflow

1. Open your n8n instance
2. Go to **Workflows** → **Import from File**
3. Select `n8n_voice_ai_agent.json`
4. Click **Import**

### Step 2: Configure Credentials

#### OpenAI API
1. Go to **Settings** → **Credentials**
2. Click **Add Credential**
3. Search for **OpenAI API**
4. Enter your OpenAI API key
5. Name it `OpenAI API` (or update the workflow to match your credential name)

#### Tavily API (Optional - for Web Search)
1. Go to **Settings** → **Credentials**
2. Click **Add Credential**
3. Search for **Header Auth**
4. Set Header Name: `Authorization`
5. Set Header Value: `Bearer YOUR_TAVILY_API_KEY`
6. Name it `Tavily API`

### Step 3: Activate the Workflow

1. Open the imported workflow
2. Click the **Active** toggle in the top right
3. Note the webhook URL displayed

## Usage

### API Endpoint

Once activated, your Voice AI Agent is available at:

```
POST https://your-n8n-instance.com/webhook/voice-ai-agent
```

### Request Format

Send a `multipart/form-data` request with an audio file:

```bash
curl -X POST \
  'https://your-n8n-instance.com/webhook/voice-ai-agent' \
  -H 'Content-Type: multipart/form-data' \
  -H 'x-session-id: user-123' \
  -F 'audio=@your-audio-file.mp3'
```

### Supported Audio Formats

- MP3 (.mp3)
- WAV (.wav)
- WebM (.webm)
- M4A (.m4a)
- OGG (.ogg)

### Response

The API returns:
- **Body**: MP3 audio file with the AI's spoken response
- **Headers**:
  - `Content-Type: audio/mpeg`
  - `X-Transcription`: The transcribed user input
  - `X-AI-Response`: The AI's text response

### Session Management

Use the `x-session-id` header to maintain conversation context:

```bash
# First message
curl -X POST ... -H 'x-session-id: user-123' -F 'audio=@question1.mp3'

# Follow-up (maintains context)
curl -X POST ... -H 'x-session-id: user-123' -F 'audio=@question2.mp3'
```

## Available Tools

The AI Agent has access to these tools:

| Tool | Description |
|------|-------------|
| **Get Current Time** | Returns current date, time, and timezone |
| **Web Search** | Searches the web for current information (requires Tavily API) |
| **Calculator** | Performs mathematical calculations |

## Customization

### Change the AI Voice

Edit the **Text to Speech (TTS)** node and change the `voice` parameter:
- `alloy` - Neutral and balanced
- `echo` - Warm and clear
- `fable` - Expressive and engaging
- `onyx` - Deep and authoritative
- `nova` - Friendly and upbeat
- `shimmer` - Soft and gentle

### Modify System Prompt

Edit the **AI Agent (GPT-4)** node and update the `systemMessage`:

```javascript
"You are a helpful Voice AI Assistant..."
```

### Add Custom Tools

1. Add a new **Tool** node (Code, HTTP Request, etc.)
2. Connect it to the AI Agent's `ai_tool` input
3. Configure the tool with name, description, and logic

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 400 - No audio file | Request missing audio | Include audio file in form-data |
| 401 - Unauthorized | Invalid API key | Check OpenAI credentials |
| 500 - Server error | Processing failed | Check n8n logs for details |

## Example Integration (JavaScript)

```javascript
async function sendVoiceMessage(audioBlob, sessionId) {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'recording.webm');
  
  const response = await fetch('https://your-n8n-instance.com/webhook/voice-ai-agent', {
    method: 'POST',
    headers: {
      'x-session-id': sessionId
    },
    body: formData
  });
  
  if (!response.ok) {
    throw new Error(`Error: ${response.status}`);
  }
  
  const audioResponse = await response.blob();
  const transcription = response.headers.get('X-Transcription');
  const aiText = response.headers.get('X-AI-Response');
  
  return { audioResponse, transcription, aiText };
}
```

## Example Integration (Python)

```python
import requests

def send_voice_message(audio_path: str, session_id: str) -> dict:
    url = "https://your-n8n-instance.com/webhook/voice-ai-agent"
    
    with open(audio_path, 'rb') as audio_file:
        files = {'audio': audio_file}
        headers = {'x-session-id': session_id}
        
        response = requests.post(url, files=files, headers=headers)
        response.raise_for_status()
        
        return {
            'audio': response.content,
            'transcription': response.headers.get('X-Transcription'),
            'ai_response': response.headers.get('X-AI-Response')
        }

# Usage
result = send_voice_message('question.mp3', 'user-123')
with open('response.mp3', 'wb') as f:
    f.write(result['audio'])
```

## Cost Estimation

| Service | Approximate Cost |
|---------|-----------------|
| Whisper (STT) | ~$0.006 per minute of audio |
| GPT-4o | ~$0.005 per 1K tokens (input) + $0.015 per 1K tokens (output) |
| TTS | ~$0.015 per 1K characters |

**Example**: A 30-second voice interaction typically costs ~$0.01-0.03

## Troubleshooting

### Webhook not accessible
- Ensure n8n is running and accessible
- Check if the workflow is activated
- Verify firewall/network settings

### Audio not processing
- Verify the audio format is supported
- Check that the audio file is not corrupted
- Ensure OpenAI credentials are valid

### Memory not persisting
- Include `x-session-id` header in requests
- Check memory buffer configuration

## License

This workflow is provided as-is for educational and commercial use.

---

Created with n8n - The workflow automation platform
