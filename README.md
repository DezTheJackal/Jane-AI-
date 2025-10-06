🤖 Modern AI Assistant - Installation & Usage Guide
📋 Features
✨ Core Features:

🎤 Voice recognition (speech-to-text)
🔊 Text-to-speech responses
🌐 Web searches and site opening
⏰ Time and date queries
🤖 OpenAI GPT integration for natural conversations
💬 Context-aware conversations
🖥️ Modern GUI interface
⌨️ Terminal mode support

🚀 Quick Start
1. Install Dependencies
bash# Install required packages
pip install pyttsx3 SpeechRecognition pyaudio openai

# For Linux/Mac, you might need:
pip install PyObjC  # macOS only

Note: PyAudio installation may require additional setup:

Windows: Usually works directly
macOS: brew install portaudio then pip install pyaudio
Linux: sudo apt-get install python3-pyaudio portaudio19-dev

2. Download Files
Save these two files in the same directory:

ai_assistant.py (main application)
ai_assistant_gui.py (GUI interface)

3. Configure OpenAI (Optional but Recommended)
   # Run configuration
python ai_assistant.py --config

# Enter your OpenAI API key when prompted
# Get your key from: https://platform.openai.com/api-keys

💻 Usage
GUI Mode (Default)
# Launch with graphical interface
python ai_assistant.py

GUI Features:

Type messages in the input box
Press Enter to send (Shift+Enter for new line)
Click "Voice" button for voice input
Modern dark theme interface
Real-time status updates

Terminal Mode
# Launch in terminal only
python ai_assistant.py --terminal
# or
python ai_assistant.py -t

Terminal Commands:

Type your questions directly
Type listen to use voice input
Type exit to quit

🎯 Example Commands
"What time is it?"
"What's today's date?"
"Open Google"
"Open YouTube"
"Search for Python tutorials"

Web Navigation
"Open GitHub"
"Open LinkedIn"
"Open Gmail"
"Search for weather forecast"
"YouTube Python programming"

AI Conversations (with OpenAI)
"Explain quantum computing"
"Write a poem about nature"
"Help me debug this code"
"What's the meaning of life?"
"Tell me a joke"

⚙️ Configuration
Config File Location

Windows: C:\Users\YourName\.ai_assistant_config.json
macOS/Linux: ~/.ai_assistant_config.json

Manual Configuration
Edit the config file directly:
{
  "voice_rate": 175,
  "voice_volume": 0.9,
  "voice_index": 1,
  "openai_api_key": "your-api-key-here",
  "assistant_name": "Assistant"
}

Voice Settings

voice_rate: Speech speed (150-200 recommended)
voice_volume: Volume level (0.0-1.0)
voice_index: Voice selection (0=male, 1=female typically)

🔧 Troubleshooting
"N# Windows
pip install pipwin
pipwin install pyaudio

# macOS
brew install portaudio
pip install pyaudio

# Linux
sudo apt-get install python3-pyaudioo module named 'pyaudio'"

OpenAI API Error"

Check your API key is correct
Ensure you have credits in your OpenAI account
Check internet connection

Voice Recognition Not Working

Check microphone permissions
Ensure microphone is properly connected
Try adjusting energy_threshold in code

No Speech Output

Check system volume
Verify speakers/headphones are connected
Test with: python -c "import pyttsx3; e=pyttsx3.init(); e.say('test'); e.runAndWait()"

🎨 Customization
Change Assistant Name

python ai_assistant.py --config
# Enter new name when prompted

Modify Colors (GUI)
Edit ai_assistant_gui.py and change color variables:

pythonself.bg_color = "#1e1e2e"      # Background
self.accent_color = "#89b4fa"   # Accent color
self.button_color = "#89b4fa"   # Button color

Add Custom Commands
Edit process_command() method in ai_assistant.py:

📱 Running on Startup (Optional)
Windows

Press Win + R
Type shell:startup
Create shortcut to ai_assistant.py

macOS

Open System Preferences → Users & Groups
Click Login Items
Add ai_assistant.py

Linux
Add to ~/.bashrc or create systemd service
🔒 Security Notes

API keys are stored locally in config file
Never share your OpenAI API key
Config file has user-only read permissions
No data is stored or transmitted except to OpenAI

💡 Tips

Better Recognition: Speak clearly and at normal pace
Context: OpenAI remembers last 10 messages
Commands: Simple commands work best ("open X", "search Y")
Voice Input: Wait for "Listening..." before speaking
Terminal Mode: Faster for quick queries

🆘 Getting Help
If you encounter issues:

Check error messages in terminal
Verify all dependencies are installed
Test microphone with other apps
Check OpenAI API status
Review configuration file

📈 Performance

Startup Time: < 2 seconds
Response Time: 1-3 seconds (depends on OpenAI)
Memory Usage: ~50-100 MB
CPU Usage: Minimal (spikes during speech processing)

🔄 Updates
To update:
pip install --upgrade openai pyttsx3 SpeechRecognition

Enjoy your AI Assistant! 🚀
