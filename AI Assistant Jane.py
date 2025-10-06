"""
Modern AI Virtual Assistant with GUI and Terminal Support
Features: OpenAI integration, voice recognition, sleek interface
Author: Enhanced version
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

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI not installed. Run: pip install openai")

class AIAssistant:
    def __init__(self, use_gui=True):
        """Initialize the AI Assistant"""
        self.use_gui = use_gui
        self.config_file = Path.home() / ".ai_assistant_config.json"
        self.config = self.load_config()
        
        # Initialize text-to-speech
        self.engine = pyttsx3.init()
        self.setup_voice()
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.8
        self.recognizer.energy_threshold = 300
        
        # Initialize OpenAI if available
        self.client = None
        if OPENAI_AVAILABLE and self.config.get('openai_api_key'):
            try:
                self.client = OpenAI(api_key=self.config['openai_api_key'])
            except Exception as e:
                print(f"OpenAI initialization failed: {e}")
        
        # Conversation history for context
        self.conversation_history = []
        
        # Command queue for thread-safe operations
        self.command_queue = queue.Queue()
        self.running = True
        
    def load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'voice_rate': 175,
            'voice_volume': 0.9,
            'voice_index': 1,
            'openai_api_key': '',
            'assistant_name': 'Assistant'
        }
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Failed to save config: {e}")
    
    def setup_voice(self):
        """Configure text-to-speech voice"""
        voices = self.engine.getProperty('voices')
        if voices:
            voice_idx = min(self.config.get('voice_index', 1), len(voices) - 1)
            self.engine.setProperty('voice', voices[voice_idx].id)
        self.engine.setProperty('rate', self.config.get('voice_rate', 175))
        self.engine.setProperty('volume', self.config.get('voice_volume', 0.9))
    
    def speak(self, text, print_text=True):
        """Text-to-speech output"""
        if print_text:
            print(f"🤖 {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")
    
    def listen(self):
        """Listen for voice input"""
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            print("🔄 Recognizing...")
            query = self.recognizer.recognize_google(audio, language='en-US')
            print(f"👤 You said: {query}")
            return query.lower()
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def ask_openai(self, query):
        """Query OpenAI API with conversation context"""
        if not self.client:
            return "OpenAI is not configured. Please set your API key."
        
        try:
            # Add user message to history
            self.conversation_history.append({"role": "user", "content": query})
            
            # Keep only last 10 messages for context
            context = self.conversation_history[-10:]
            
            # Add system message
            messages = [
                {"role": "system", "content": "You are a helpful, friendly AI assistant. Keep responses concise and natural."}
            ] + context
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content.strip()
            
            # Add assistant response to history
            self.conversation_history.append({"role": "assistant", "content": answer})
            
            return answer
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
    
    def get_time(self):
        """Get current time"""
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"The time is {time_str}"
    
    def get_date(self):
        """Get current date"""
        now = datetime.datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        return f"Today is {date_str}"
    
    def greet(self):
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
    
    def process_command(self, query):
        """Process user command"""
        if not query:
            return None
        
        query = query.lower().strip()
        
        # Exit commands
        if any(word in query for word in ['exit', 'quit', 'bye', 'goodbye']):
            return "exit"
        
        # Time
        if 'time' in query:
            return self.get_time()
        
        # Date
        if any(word in query for word in ['date', 'day', 'today']):
            return self.get_date()
        
        # Open Google
        if 'open google' in query:
            search_query = query.replace('open google', '').strip()
            if search_query:
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
                return "Opening Google search"
            else:
                webbrowser.open("https://www.google.com")
                return "Opening Google"
        
        # Open YouTube
        if 'open youtube' in query or 'youtube' in query:
            search_query = query.replace('open youtube', '').replace('youtube', '').strip()
            if search_query:
                webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
                return "Opening YouTube search"
            else:
                webbrowser.open("https://www.youtube.com")
                return "Opening YouTube"
        
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
            if site in query:
                webbrowser.open(url)
                return f"Opening {site.title()}"
        
        # Search web
        if any(word in query for word in ['search', 'look up', 'find']):
            search_query = query
            for word in ['search', 'search for', 'look up', 'find']:
                search_query = search_query.replace(word, '').strip()
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            return "Searching the web"
        
        # Use OpenAI for general queries
        if self.client:
            return self.ask_openai(query)
        else:
            return "I can help with time, date, opening websites, and web searches. For advanced AI features, please configure your OpenAI API key."
    
    def run_terminal(self):
        """Run in terminal mode"""
        print("\n" + "="*60)
        print("🤖 AI ASSISTANT - Terminal Mode")
        print("="*60)
        print("\nCommands:")
        print("  - Say 'listen' to use voice input")
        print("  - Type your questions directly")
        print("  - Say 'exit' to quit")
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
                print(f"❌ Error: {e}")
    
    def run_gui(self):
        """Run with GUI (imported separately to keep dependencies optional)"""
        try:
            from ai_assistant_gui import AssistantGUI
            gui = AssistantGUI(self)
            gui.run()
        except ImportError:
            print("GUI dependencies not available. Running in terminal mode.")
            self.run_terminal()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Virtual Assistant')
    parser.add_argument('--terminal', '-t', action='store_true', 
                       help='Run in terminal mode')
    parser.add_argument('--config', '-c', action='store_true',
                       help='Configure OpenAI API key')
    
    args = parser.parse_args()
    
    assistant = AIAssistant(use_gui=not args.terminal)
    
    if args.config:
        print("\n🔧 Configuration")
        print("="*60)
        api_key = input("Enter your OpenAI API key (or press Enter to skip): ").strip()
        if api_key:
            assistant.config['openai_api_key'] = api_key
            assistant.save_config()
            print("✅ API key saved!")
        
        name = input("Enter assistant name (default: Assistant): ").strip()
        if name:
            assistant.config['assistant_name'] = name
            assistant.save_config()
            print(f"✅ Assistant name set to: {name}")
        
        print("\n" + "="*60)
        return
    
    if args.terminal:
        assistant.run_terminal()
    else:
        assistant.run_gui()

if __name__ == "__main__":
    main()
     

