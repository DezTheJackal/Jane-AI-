"""
Modern AI Virtual Assistant with GUI and Terminal Support
Features: OpenAI integration, voice recognition, sleek interface

Version: 2.1.0
Status: Stable
Last Updated: November 2025
"""

import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import sys
import json
from pathlib import Path
import threading
import queue
import logging
from typing import Optional, Dict, Any

# Version information
__version__ = "2.1.0"
__status__ = "Stable"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI not installed. Run: pip install openai")

class AIAssistant:
    def __init__(self, use_gui: bool = True):
        """Initialize the AI Assistant"""
        self.use_gui = use_gui
        self.config_file = Path.home() / ".ai_assistant_config.json"
        self.config = self.load_config()
        
        # Initialize text-to-speech with error handling
        try:
            self.engine = pyttsx3.init()
            self.setup_voice()
        except Exception as e:
            logger.error(f"Text-to-speech initialization failed: {e}")
            self.engine = None
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.8
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        
        # Initialize OpenAI if available
        self.client = None
        if OPENAI_AVAILABLE and self.config.get('openai_api_key'):
            try:
                self.client = OpenAI(api_key=self.config['openai_api_key'])
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"OpenAI initialization failed: {e}")
        
        # Conversation history for context
        self.conversation_history = []
        
        # Command queue for thread-safe operations
        self.command_queue = queue.Queue()
        self.running = True
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        default_config = {
            'voice_rate': 175,
            'voice_volume': 0.9,
            'voice_index': 1,
            'openai_api_key': '',
            'assistant_name': 'Assistant',
            'model': 'gpt-3.5-turbo',
            'max_history': 10
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    default_config.update(loaded_config)
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
        
        return default_config
    
    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            logger.info("Configuration saved successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False
    
    def setup_voice(self):
        """Configure text-to-speech voice"""
        if not self.engine:
            return
        
        try:
            voices = self.engine.getProperty('voices')
            if voices:
                voice_idx = self.config.get('voice_index', 1)
                voice_idx = min(voice_idx, len(voices) - 1)
                self.engine.setProperty('voice', voices[voice_idx].id)
            
            self.engine.setProperty('rate', self.config.get('voice_rate', 175))
            self.engine.setProperty('volume', self.config.get('voice_volume', 0.9))
        except Exception as e:
            logger.error(f"Voice setup failed: {e}")
    
    def speak(self, text: str, print_text: bool = True):
        """Text-to-speech output"""
        if print_text:
            print(f"🤖 {text}")
        
        if not self.engine:
            return
        
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Speech error: {e}")
    
    def listen(self) -> Optional[str]:
        """Listen for voice input"""
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                except sr.WaitTimeoutError:
                    logger.warning("Listening timeout - no speech detected")
                    return None
                
            print("🔄 Recognizing...")
            query = self.recognizer.recognize_google(audio, language='en-US')
            print(f"👤 You said: {query}")
            return query.lower()
            
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            print("❌ Speech recognition service unavailable")
            return None
        except Exception as e:
            logger.error(f"Listening error: {e}")
            return None
    
    def ask_openai(self, query: str) -> str:
        """Query OpenAI API with conversation context"""
        if not self.client:
            return "OpenAI is not configured. Please set your API key using: python ai_assistant.py --config"
        
        try:
            # Add user message to history
            self.conversation_history.append({"role": "user", "content": query})
            
            # Keep only last N messages for context
            max_history = self.config.get('max_history', 10)
            context = self.conversation_history[-max_history:]
            
            # Add system message
            messages = [
                {
                    "role": "system", 
                    "content": "You are a helpful, friendly AI assistant. Keep responses concise and natural."
                }
            ] + context
            
            # Call OpenAI API
            model = self.config.get('model', 'gpt-3.5-turbo')
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content.strip()
            
            # Add assistant response to history
            self.conversation_history.append({"role": "assistant", "content": answer})
            
            return answer
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def get_time(self) -> str:
        """Get current time"""
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"The time is {time_str}"
    
    def get_date(self) -> str:
        """Get current date"""
        now = datetime.datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        return f"Today is {date_str}"
    
    def greet(self) -> str:
        """Greet the user"""
        hour = datetime.datetime.now().hour
        if hour < 12:
            greeting = "Good morning"
        elif hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        
        name = self.config.get('assistant_name', 'Assistant')
        return f"{greeting}! I'm {name}, your AI assistant. How can I help you?"
    
    def process_command(self, query: str) -> Optional[str]:
        """Process user command"""
        if not query:
            return None
        
        query = query.lower().strip()
        
        # Exit commands
        if any(word in query for word in ['exit', 'quit', 'bye', 'goodbye']):
            return "exit"
        
        # Help command
        if 'help' in query or 'what can you do' in query:
            return self.get_help()
        
        # Time
        if 'time' in query:
            return self.get_time()
        
        # Date
        if any(word in query for word in ['date', 'day', 'today']) and 'update' not in query:
            return self.get_date()
        
        # Open Google
        if 'open google' in query or query.startswith('google '):
            search_query = query.replace('open google', '').replace('google', '').strip()
            if search_query:
                try:
                    webbrowser.open(f"https://www.google.com/search?q={search_query}")
                    return f"Searching Google for: {search_query}"
                except Exception as e:
                    logger.error(f"Failed to open browser: {e}")
                    return "Sorry, I couldn't open your browser"
            else:
                try:
                    webbrowser.open("https://www.google.com")
                    return "Opening Google"
                except Exception as e:
                    logger.error(f"Failed to open browser: {e}")
                    return "Sorry, I couldn't open your browser"
        
        # Open YouTube
        if 'youtube' in query:
            search_query = query.replace('open youtube', '').replace('youtube', '').strip()
            if search_query:
                try:
                    webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
                    return f"Searching YouTube for: {search_query}"
                except Exception as e:
                    logger.error(f"Failed to open browser: {e}")
                    return "Sorry, I couldn't open your browser"
            else:
                try:
                    webbrowser.open("https://www.youtube.com")
                    return "Opening YouTube"
                except Exception as e:
                    logger.error(f"Failed to open browser: {e}")
                    return "Sorry, I couldn't open your browser"
        
        # Open websites
        websites = {
            'github': 'https://github.com',
            'linkedin': 'https://linkedin.com',
            'twitter': 'https://twitter.com',
            'facebook': 'https://facebook.com',
            'reddit': 'https://reddit.com',
            'gmail': 'https://gmail.com'
        }
        
        for site, url in websites.items():
            if site in query and 'open' in query:
                try:
                    webbrowser.open(url)
                    return f"Opening {site.title()}"
                except Exception as e:
                    logger.error(f"Failed to open {site}: {e}")
                    return f"Sorry, I couldn't open {site}"
        
        # Search web
        if any(word in query for word in ['search for', 'search', 'look up', 'find']):
            search_query = query
            for word in ['search for', 'search', 'look up', 'find']:
                search_query = search_query.replace(word, '').strip()
            if search_query:
                try:
                    webbrowser.open(f"https://www.google.com/search?q={search_query}")
                    return f"Searching for: {search_query}"
                except Exception as e:
                    logger.error(f"Failed to search: {e}")
                    return "Sorry, I couldn't perform the search"
        
        # Use OpenAI for general queries
        if self.client:
            return self.ask_openai(query)
        else:
            return ("I can help with time, date, opening websites, and web searches. "
                   "For advanced AI features, please configure your OpenAI API key using: "
                   "python ai_assistant.py --config")
    
    def get_help(self) -> str:
        """Return help message"""
        return """Available commands:
• Time: "what time is it?"
• Date: "what's the date?"
• Search: "search for [topic]"
• Websites: "open google/youtube/github/etc"
• Exit: "exit" or "quit"
• Help: "help" or "what can you do?"
""" + ("• AI Chat: Ask me anything!" if self.client else "• Configure OpenAI for AI chat features")
    
    def run_terminal(self):
        """Run in terminal mode"""
        print("\n" + "="*60)
        print("🤖 AI ASSISTANT - Terminal Mode")
        print("="*60)
        print("\nCommands:")
        print("  - Say 'listen' to use voice input")
        print("  - Type your questions directly")
        print("  - Say 'exit' to quit")
        print("  - Say 'help' for available commands")
        print("\n" + "="*60 + "\n")
        
        # Greet user
        greeting = self.greet()
        self.speak(greeting)
        
        while self.running:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                # Voice input mode
                if user_input.lower() == 'listen':
                    query = self.listen()
                    if query:
                        response = self.process_command(query)
                    else:
                        continue
                else:
                    response = self.process_command(user_input)
                
                if response == "exit":
                    self.speak("Goodbye! Have a great day!")
                    break
                elif response:
                    self.speak(response)
                    
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted by user")
                break
            except Exception as e:
                logger.error(f"Error in terminal loop: {e}")
                print(f"❌ Error: {e}")
    
    def run_gui(self):
        """Run with GUI (imported separately to keep dependencies optional)"""
        try:
            from ai_assistant_gui import AssistantGUI
            gui = AssistantGUI(self)
            gui.run()
        except ImportError as e:
            logger.error(f"GUI import failed: {e}")
            print("GUI dependencies not available. Running in terminal mode.")
            print("Make sure ai_assistant_gui.py is in the same directory.")
            self.run_terminal()
        except Exception as e:
            logger.error(f"GUI error: {e}")
            print(f"GUI error: {e}")
            print("Running in terminal mode instead.")
            self.run_terminal()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='AI Virtual Assistant',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ai_assistant.py              # Run with GUI
  python ai_assistant.py --terminal   # Run in terminal mode
  python ai_assistant.py --config     # Configure settings
        """
    )
    parser.add_argument('--terminal', '-t', action='store_true', 
                       help='Run in terminal mode')
    parser.add_argument('--config', '-c', action='store_true',
                       help='Configure OpenAI API key and settings')
    
    args = parser.parse_args()
    
    assistant = AIAssistant(use_gui=not args.terminal)
    
    if args.config:
        print("\n🔧 Configuration")
        print("="*60)
        
        api_key = input("Enter your OpenAI API key (or press Enter to skip): ").strip()
        if api_key:
            assistant.config['openai_api_key'] = api_key
            if assistant.save_config():
                print("✅ API key saved!")
        
        name = input("Enter assistant name (default: Assistant): ").strip()
        if name:
            assistant.config['assistant_name'] = name
            if assistant.save_config():
                print(f"✅ Assistant name set to: {name}")
        
        model = input("Enter OpenAI model (default: gpt-3.5-turbo): ").strip()
        if model:
            assistant.config['model'] = model
            if assistant.save_config():
                print(f"✅ Model set to: {model}")
        
        print("\n" + "="*60)
        return
    
    try:
        if args.terminal:
            assistant.run_terminal()
        else:
            assistant.run_gui()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
