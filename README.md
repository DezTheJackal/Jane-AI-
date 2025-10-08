# 🤖 AI Virtual Assistant - Complete Guide

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com)

A powerful, modern AI virtual assistant with voice recognition, natural language processing, and a beautiful GUI interface. Control your computer, search the web, and have intelligent conversations—all through voice commands or text input.

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Detailed Installation](#-detailed-installation)
- [Usage Guide](#-usage-guide)
- [Command Reference](#-command-reference)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Advanced Usage](#-advanced-usage)
- [API Reference](#-api-reference)
- [FAQ](#-faq)

---

## ✨ Features

### Core Capabilities
- 🎤 **Voice Recognition** - Natural speech-to-text powered by Google Speech Recognition
- 🔊 **Text-to-Speech** - Responsive voice feedback with customizable voices
- 🤖 **OpenAI Integration** - Advanced AI conversations using GPT models
- 💬 **Context Awareness** - Remembers conversation history for natural dialogue
- 🖥️ **Modern GUI** - Sleek, dark-themed interface built with Tkinter
- ⌨️ **Terminal Mode** - Lightweight command-line interface option

### Functionality
- ⏰ Time and date queries
- 🌐 Web searches (Google, YouTube, Wikipedia)
- 🔗 Quick website access (GitHub, LinkedIn, Gmail, etc.)
- 📧 Email sending capabilities
- 🎵 Music and video playback
- 💻 Application launching (VS Code, Teams, etc.)
- 📝 Custom command processing
- 🔄 Conversation history tracking

### Interface Options
- **GUI Mode**: Beautiful graphical interface with real-time status updates
- **Terminal Mode**: Fast, keyboard-friendly command-line interface
- **Voice Mode**: Hands-free interaction through microphone
- **Hybrid Mode**: Combine text and voice input seamlessly

---

## 🚀 Quick Start

### Automated Setup (Recommended)

**One command to install everything:**

```bash
# Download and run the setup script
python setup.py
```

The setup script will:
1. ✓ Check Python version compatibility
2. ✓ Install all dependencies automatically
3. ✓ Create necessary directories
4. ✓ Configure the assistant
5. ✓ Test the installation
6. ✓ Create launcher shortcuts

**That's it!** After setup completes, run:

```bash
python ai_assistant.py
```

---

## 📦 Detailed Installation

### Prerequisites

**Required:**
- Python 3.7 or higher
- Working microphone (for voice input)
- Internet connection (for web features and OpenAI)

**Operating Systems:**
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu, Fedora, Arch, etc.)

### Method 1: Automated (Easiest)

```bash
# Clone or download the repository
git clone https://github.com/yourusername/ai-assistant.git
cd ai-assistant

# Run the setup script
python setup.py
```

### Method 2: Manual Installation

#### Step 1: Install Python Dependencies

```bash
# Install core packages
pip install pyttsx3 SpeechRecognition openai wikipedia requests
```

#### Step 2: Install PyAudio (Platform-Specific)

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

**Linux (Fedora):**
```bash
sudo yum install python3-pyaudio portaudio-devel
pip install pyaudio
```

**Linux (Arch):**
```bash
sudo pacman -S python-pyaudio portaudio
pip install pyaudio
```

#### Step 3: Download Assistant Files

Download these files to the same directory:
- `ai_assistant.py` (main application)
- `ai_assistant_gui.py` (GUI interface)
- `setup.py` (setup script)

#### Step 4: Create Configuration

```bash
python ai_assistant.py --config
```

Follow the prompts to configure your assistant.

---

## 📖 Usage Guide

### Starting the Assistant

#### GUI Mode (Default)
```bash
python ai_assistant.py
```

**Features:**
- Modern dark-themed interface
- Type or speak your commands
- Real-time status updates
- Message history
- Easy-to-use buttons

#### Terminal Mode
```bash
python ai_assistant.py --terminal
# or
python ai_assistant.py -t
```

**Features:**
- Lightweight and fast
- Keyboard-friendly
- Perfect for SSH sessions
- Low resource usage

#### Configuration Mode
```bash
python ai_assistant.py --config
```

### Basic Interaction

#### Text Input
1. Type your question or command
2. Press Enter to submit
3. Wait for the response

#### Voice Input
1. Click the "Voice" button (GUI) or type "listen" (Terminal)
2. Wait for "Listening..." prompt
3. Speak clearly into your microphone
4. Wait for recognition and response

---

## 🎯 Command Reference

### Time & Date Commands

```
"What time is it?"
"What's the time?"
"Tell me the time"

"What's today's date?"
"What day is it?"
"Tell me the date"
```

**Example Response:**
```
🤖 The time is 3:45 PM
🤖 Today is Monday, October 08, 2025
```

---

### Web Navigation

#### Google Search
```
"Open Google"
"Search for Python tutorials"
"Google machine learning"
"Find restaurants near me"
```

#### YouTube
```
"Open YouTube"
"YouTube Python programming"
"Play music on YouTube"
"Search YouTube for cat videos"
```

#### Wikipedia
```
"Wikipedia quantum computing"
"Look up Einstein on Wikipedia"
"What is machine learning"
```

#### Quick Website Access
```
"Open GitHub"          → github.com
"Open LinkedIn"        → linkedin.com
"Open Gmail"           → gmail.com
"Open Twitter"         → twitter.com
"Open Facebook"        → facebook.com
"Open Reddit"          → reddit.com
```

---

### AI Conversations (OpenAI)

**Note:** Requires OpenAI API key configuration

```
"Explain quantum computing"
"Write a poem about nature"
"Help me debug this code"
"What's the meaning of life?"
"Tell me a joke"
"Summarize the theory of relativity"
"How do I learn Python?"
"What's the weather like?" (requires internet)
```

**Example Conversation:**
```
👤 You: Explain recursion simply
🤖 Recursion is when a function calls itself to solve a problem 
   by breaking it into smaller, similar sub-problems. Think of 
   it like looking into two mirrors facing each other - each 
   reflection contains another reflection.

👤 You: Give me an example
🤖 Here's a simple example: calculating factorial. 
   factorial(5) = 5 × factorial(4), which calls factorial(3), 
   and so on until factorial(1) = 1. Then it multiplies back up.
```

---

### System Commands

#### Exit Commands
```
"Exit"
"Quit"
"Bye"
"Goodbye"
```

#### Help
```
"Help"
"What can you do?"
"Commands"
```

---

### Media Playback

**Note:** Requires media directories configured

```
"Play music"           → Plays first song in music folder
"Play video"           → Plays first video in videos folder
"Play song on cloud"   → Opens SoundCloud search
```

---

### Application Launching

```
"Open VS Code"
"Open Code Blocks"
"Open Teams"
"Open command prompt"
"Open terminal"
```

---

## ⚙️ Configuration

### Configuration File Location

- **Windows**: `C:\Users\YourName\.ai_assistant_config.json`
- **macOS/Linux**: `~/.ai_assistant_config.json`

### Configuration Options

```json
{
  "voice_rate": 175,
  "voice_volume": 0.9,
  "voice_index": 1,
  "openai_api_key": "your-api-key-here",
  "assistant_name": "Assistant",
  "directories": {
    "base": "/path/to/AIAssistant",
    "music": "/path/to/AIAssistant/music",
    "videos": "/path/to/AIAssistant/videos",
    "documents": "/path/to/AIAssistant/documents",
    "logs": "/path/to/AIAssistant/logs"
  },
  "preferences": {
    "auto_listen": false,
    "verbose_mode": true,
    "save_logs": true
  }
}
```

### Voice Settings

| Setting | Description | Range | Default |
|---------|-------------|-------|---------|
| `voice_rate` | Speech speed | 100-250 | 175 |
| `voice_volume` | Volume level | 0.0-1.0 | 0.9 |
| `voice_index` | Voice selection | 0-N | 1 |

**Voice Index:**
- `0` - Usually male voice
- `1` - Usually female voice
- Higher numbers for additional voices (if available)

### OpenAI Configuration

1. **Get API Key:**
   - Visit https://platform.openai.com/api-keys
   - Create new API key
   - Copy the key (you won't see it again!)

2. **Configure Assistant:**
   ```bash
   python ai_assistant.py --config
   ```
   Or manually edit the config file.

3. **Test Configuration:**
   ```bash
   python ai_assistant.py
   # Ask: "Tell me a joke"
   ```

### Custom Directories

Edit the config file to change media directories:

```json
{
  "directories": {
    "music": "/Users/yourname/Music",
    "videos": "/Users/yourname/Videos",
    "documents": "/Users/yourname/Documents"
  }
}
```

---

## 🔧 Troubleshooting

### Common Issues

#### Issue: "No module named 'pyaudio'"

**Solution:**

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

---

#### Issue: "OpenAI API Error" or "Invalid API Key"

**Solutions:**
1. Check your API key is correct
2. Verify you have credits: https://platform.openai.com/account/usage
3. Test your key:
   ```bash
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer YOUR_API_KEY"
   ```
4. Reconfigure:
   ```bash
   python ai_assistant.py --config
   ```

---

#### Issue: Voice Recognition Not Working

**Checklist:**
- ✓ Microphone is connected and working
- ✓ Microphone permissions granted to Terminal/Python
- ✓ PyAudio is installed correctly
- ✓ No other app is using the microphone
- ✓ Background noise is minimal

**Test Microphone:**
```bash
# Test system recognition
python -c "import speech_recognition as sr; r=sr.Recognizer(); print('Microphones:', sr.Microphone.list_microphone_names())"
```

**Adjust Sensitivity:**
Edit `ai_assistant.py`:
```python
self.recognizer.energy_threshold = 300  # Increase for noisy environments
self.recognizer.pause_threshold = 0.8  # Time before considering speech finished
```

---

#### Issue: No Speech Output

**Solutions:**
1. Check system volume
2. Verify speakers/headphones are connected
3. Test text-to-speech:
   ```bash
   python -c "import pyttsx3; e=pyttsx3.init(); e.say('test'); e.runAndWait()"
   ```
4. Try different voice:
   ```bash
   python ai_assistant.py --config
   # Change voice_index to 0 or 2
   ```

---

#### Issue: GUI Won't Start

**Solutions:**
1. Try terminal mode:
   ```bash
   python ai_assistant.py --terminal
   ```
2. Check Tkinter installation:
   ```bash
   python -c "import tkinter; print('Tkinter OK')"
   ```
3. Install Tkinter:
   - **Ubuntu/Debian**: `sudo apt-get install python3-tk`
   - **Fedora**: `sudo yum install python3-tkinter`
   - **macOS**: Included with Python
   - **Windows**: Included with Python

---

#### Issue: "Command Not Found" or "Unrecognized"

**Solutions:**
1. Speak more clearly and slowly
2. Check available commands in this README
3. Ensure OpenAI is configured for general queries
4. Use simpler, more direct phrasing

**Examples:**
- ❌ "Could you possibly open up Google for me please?"
- ✅ "Open Google"

---

### Performance Issues

#### Slow Response Time

**Causes & Solutions:**
- **Internet Speed**: OpenAI requires internet; check connection
- **API Rate Limits**: Reduce request frequency
- **System Resources**: Close unnecessary applications
- **Old Hardware**: Consider terminal mode (lighter weight)

#### High CPU Usage

**Solutions:**
1. Use terminal mode instead of GUI
2. Disable auto-listen feature
3. Close other resource-intensive apps
4. Update Python to latest version

---

### Platform-Specific Issues

#### macOS

**Microphone Permission Denied:**
```
System Preferences → Security & Privacy → Privacy → Microphone
→ Enable for Terminal/Python
```

**PyAudio Installation Fails:**
```bash
xcode-select --install
brew install portaudio
pip install pyaudio
```

#### Windows

**PyAudio Wheel Error:**
```bash
# Use pipwin instead
pip install pipwin
pipwin install pyaudio
```

**Antivirus Blocking:**
- Add Python executable to antivirus exceptions
- Temporarily disable real-time protection during installation

#### Linux

**ALSA Errors:**
```bash
sudo apt-get install libasound2-dev
pip install pyaudio --user
```

**Permission Issues:**
```bash
# Add user to audio group
sudo usermod -a -G audio $USER
# Logout and login for changes to take effect
```

---

## 🚀 Advanced Usage

### Custom Commands

Add your own commands by editing `ai_assistant.py`:

```python
def process_command(self, query):
    # ... existing code ...
    
    # Add your custom command
    if 'custom command' in query:
        # Your custom logic here
        return "Custom response"
    
    # ... rest of code ...
```

**Example - Weather Command:**
```python
if 'weather' in query:
    import requests
    # Your weather API logic
    return f"The weather is {weather_data}"
```

### API Integration Examples

#### Adding a News API
```python
def get_news(self):
    """Fetch latest news"""
    import requests
    api_key = "your_news_api_key"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    articles = response.json()['articles'][:3]
    return f"Top news: {articles[0]['title']}"
```

#### Adding Spotify Control
```python
def play_spotify(self, song_name):
    """Control Spotify playback"""
    import spotipy
    # Spotify API integration
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(...))
    results = sp.search(q=song_name, limit=1)
    # Play track logic
```

### Extending the GUI

#### Adding Custom Buttons

Edit `ai_assistant_gui.py`:

```python
# Add a custom button
custom_btn = tk.Button(
    button_frame,
    text="Custom",
    command=self.custom_action,
    **button_style
)
custom_btn.pack(side=tk.LEFT, padx=5)

def custom_action(self):
    """Custom button action"""
    self.process_query("your custom command")
```

#### Customizing Theme

```python
# Dark theme colors
self.bg_color = "#1e1e2e"        # Background
self.fg_color = "#cdd6f4"        # Text
self.accent_color = "#89b4fa"    # Accent
self.button_color = "#89b4fa"    # Buttons
self.button_hover = "#b4befe"    # Button hover

# Light theme example
self.bg_color = "#ffffff"
self.fg_color = "#000000"
self.accent_color = "#0066cc"
```

### Automation Scripts

#### Auto-start on Boot

**Windows (Task Scheduler):**
1. Open Task Scheduler
2. Create Basic Task → Name it "AI Assistant"
3. Trigger: When I log on
4. Action: Start a program
5. Program: `pythonw.exe`
6. Arguments: `"C:\path\to\ai_assistant.py"`

**macOS (LaunchAgent):**
Create `~/Library/LaunchAgents/com.aiassistant.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.aiassistant</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/path/to/ai_assistant.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

**Linux (systemd):**
Create `~/.config/systemd/user/ai-assistant.service`:
```ini
[Unit]
Description=AI Assistant
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /path/to/ai_assistant.py --terminal
Restart=on-failure

[Install]
WantedBy=default.target
```

Enable: `systemctl --user enable ai-assistant.service`

#### Scheduled Commands

Create a script that sends commands at specific times:

```python
import schedule
import time
from ai_assistant import AIAssistant

assistant = AIAssistant()

def morning_routine():
    assistant.speak("Good morning! Here's your daily briefing.")
    # Add your morning commands

schedule.every().day.at("07:00").do(morning_routine)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 📚 API Reference

### AIAssistant Class

#### Initialization
```python
assistant = AIAssistant(use_gui=True)
```

**Parameters:**
- `use_gui` (bool): Enable GUI mode (default: True)

#### Methods

##### `speak(text, print_text=True)`
Convert text to speech output.

**Parameters:**
- `text` (str): Text to speak
- `print_text` (bool): Also print to console

**Example:**
```python
assistant.speak("Hello, how can I help you?")
```

##### `listen()`
Listen for voice input from microphone.

**Returns:**
- `str`: Recognized text (lowercase)
- `None`: If recognition failed

**Example:**
```python
query = assistant.listen()
if query:
    response = assistant.process_command(query)
```

##### `process_command(query)`
Process user command and return response.

**Parameters:**
- `query` (str): User command/query

**Returns:**
- `str`: Response text
- `"exit"`: To exit the application

**Example:**
```python
response = assistant.process_command("what time is it")
assistant.speak(response)
```

##### `ask_openai(query)`
Query OpenAI API with conversation context.

**Parameters:**
- `query` (str): User question

**Returns:**
- `str`: AI-generated response

**Example:**
```python
answer = assistant.ask_openai("Explain machine learning")
```

##### `get_time()`
Get current time formatted.

**Returns:**
- `str`: "The time is HH:MM AM/PM"

##### `get_date()`
Get current date formatted.

**Returns:**
- `str`: "Today is Weekday, Month DD, YYYY"

##### `greet()`
Generate time-appropriate greeting.

**Returns:**
- `str`: Greeting message

---

## ❓ FAQ

### General Questions

**Q: Is this free to use?**  
A: Yes! The assistant is free and open-source. However, OpenAI API usage incurs costs based on your usage.

**Q: Do I need an internet connection?**  
A: Internet is required for:
- OpenAI API calls
- Web searches
- Wikipedia queries
- Opening websites

Basic commands (time, date, local files) work offline.

**Q: How much does OpenAI cost?**  
A: GPT-3.5-turbo costs approximately $0.002 per 1000 tokens (about 750 words). Typical queries cost $0.001-0.01. Check current pricing: https://openai.com/pricing

**Q: Can I use this commercially?**  
A: Yes, but review OpenAI's terms of service for API usage restrictions.

**Q: Is my data stored or shared?**  
A: No data is stored by the assistant itself. Queries sent to OpenAI are subject to their data policy: https://openai.com/policies/privacy-policy

**Q: Can I customize the assistant's personality?**  
A: Yes! Edit the system message in `ask_openai()`:
```python
{"role": "system", "content": "You are a helpful, friendly AI assistant."}
```

### Technical Questions

**Q: Which Python version should I use?**  
A: Python 3.7+ is required. Python 3.9-3.11 recommended for best compatibility.

**Q: Can I run this on Raspberry Pi?**  
A: Yes! Follow the Linux installation instructions. Note: performance may be slower on Pi 3 or older.

**Q: Does this work with non-English languages?**  
A: Voice recognition supports many languages. Modify:
```python
query = self.recognizer.recognize_google(audio, language='es-ES')  # Spanish
```

**Q: Can I use a different AI model?**  
A: Yes! Modify the `ask_openai()` method:
```python
response = self.client.chat.completions.create(
    model="gpt-4",  # or "gpt-4-turbo-preview"
    messages=messages
)
```

**Q: How do I add more voices?**  
A: List available voices:
```python
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for idx, voice in enumerate(voices):
    print(f"{idx}: {voice.name}")
```
Then set `voice_index` in config to desired number.

**Q: Can I use this with Discord/Slack/Telegram?**  
A: Not directly, but you can integrate the `AIAssistant` class into bot frameworks.

**Q: How do I backup my configuration?**  
A: Copy the config file:
```bash
# Windows
copy %USERPROFILE%\.ai_assistant_config.json backup.json

# macOS/Linux
cp ~/.ai_assistant_config.json ~/backup.json
```

---

## 📊 Performance Benchmarks

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | Dual-core 1.5GHz | Quad-core 2.5GHz+ |
| RAM | 2GB | 4GB+ |
| Storage | 100MB | 500MB+ |
| Internet | 1 Mbps | 10 Mbps+ |

### Response Times

| Operation | Average Time |
|-----------|-------------|
| Voice Recognition | 1-3 seconds |
| OpenAI Query | 1-5 seconds |
| Local Command | < 0.5 seconds |
| Web Search | 1-2 seconds |
| Application Launch | 1-3 seconds |

---

## 🔐 Security & Privacy

### Best Practices

1. **API Key Security:**
   - Never commit API keys to Git
   - Use environment variables for production
   - Rotate keys periodically

2. **File Permissions:**
   ```bash
   chmod 600 ~/.ai_assistant_config.json
   ```

3. **Network Security:**
   - Use HTTPS for all API calls
   - Validate SSL certificates
   - Monitor API usage

4. **Data Privacy:**
   - Conversation history stored in memory only
   - No persistent logging by default
   - OpenAI retains data per their policy

### Secure Configuration

Store API key in environment variable:

```bash
# Add to ~/.bashrc or ~/.zshrc
export OPENAI_API_KEY="your-key-here"
```

Modify `ai_assistant.py`:
```python
import os
api_key = os.environ.get('OPENAI_API_KEY') or self.config.get('openai_api_key')
```

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m "Add feature"`
6. Push: `git push origin feature-name`
7. Open a Pull Request

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/ai-assistant.git
cd ai-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- OpenAI for GPT API
- Google for Speech Recognition API
- Contributors and testers
- Python community

---

## 📞 Support

- **Issues**: https://github.com/yourusername/ai-assistant/issues
- **Discussions**: https://github.com/yourusername/ai-assistant/discussions
- **Email**: support@yourproject.com

---

## 🗺️ Roadmap

### Upcoming Features
- [ ] Multi-language support
- [ ] Plugin system
- [ ] Mobile app companion
- [ ] Cloud synchronization
- [ ] Custom wake word
- [ ] Offline AI mode
- [ ] Smart home integration
- [ ] Calendar integration
- [ ] Task management
- [ ] Voice authentication

---

## 📈 Changelog

### Version 2.0.0 (Current)
- ✨ Added GUI interface
- ✨ OpenAI GPT integration
- ✨ Context-aware conversations
- ✨ Automated setup script
- 🐛 Fixed voice recognition issues
- 📝 Comprehensive documentation

### Version 1.0.0
- Initial release
- Basic voice commands
- Web navigation
- Time/date queries

---

**Made with ❤️ by the AI Assistant Team**

*For more information, visit our [GitHub repository](https://github.com/yourusername/ai-assistant)*

---

**Quick Links:**
- [Installation](#-detailed-installation)
- [Commands](#-command-reference)
- [Troubleshooting](#-troubleshooting)
- [Configuration](#-configuration)
- [FAQ](#-faq)
