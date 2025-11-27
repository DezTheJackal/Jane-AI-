"""
AI Assistant GUI Interface
FIXED VERSION - Bug fixes and improvements
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class AssistantGUI:
    def __init__(self, assistant):
        """Initialize the GUI"""
        self.assistant = assistant
        self.root = tk.Tk()
        self.root.title(f"🤖 {assistant.config.get('assistant_name', 'AI Assistant')}")
        self.root.geometry("700x600")
        self.root.minsize(600, 500)
        
        # Colors - Modern dark theme
        self.bg_color = "#1e1e2e"
        self.fg_color = "#cdd6f4"
        self.accent_color = "#89b4fa"
        self.button_color = "#89b4fa"
        self.button_hover = "#b4befe"
        self.entry_bg = "#313244"
        self.text_bg = "#181825"
        
        self.setup_ui()
        self.listening = False
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_ui(self):
        """Setup the user interface"""
        self.root.configure(bg=self.bg_color)
        
        # Title Frame
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=10, padx=20, fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text=f"🤖 {self.assistant.config.get('assistant_name', 'AI Assistant')}",
            font=("Segoe UI", 18, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack()
        
        status_text = "AI-Powered" if self.assistant.client else "Basic Mode"
        subtitle = tk.Label(
            title_frame,
            text=status_text,
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg=self.fg_color
        )
        subtitle.pack()
        
        # Chat Display
        chat_frame = tk.Frame(self.root, bg=self.bg_color)
        chat_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg=self.text_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Configure tags for colored text
        self.chat_display.tag_config("user", foreground="#a6e3a1", font=("Consolas", 11, "bold"))
        self.chat_display.tag_config("assistant", foreground="#89b4fa", font=("Consolas", 11, "bold"))
        self.chat_display.tag_config("system", foreground="#f9e2af", font=("Consolas", 10, "italic"))
        
        # Input Frame
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.input_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 12),
            bg=self.entry_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief=tk.FLAT,
            bd=5
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_entry.bind("<Return>", lambda e: self.send_message())
        self.input_entry.focus()
        
        # Button Frame
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=5, padx=20, fill=tk.X)
        
        button_style = {
            "font": ("Segoe UI", 10, "bold"),
            "bg": self.button_color,
            "fg": "#1e1e2e",
            "relief": tk.FLAT,
            "cursor": "hand2",
            "padx": 15,
            "pady": 8
        }
        
        self.voice_btn = tk.Button(
            button_frame,
            text="🎤 Voice",
            command=self.voice_input,
            **button_style
        )
        self.voice_btn.pack(side=tk.LEFT, padx=5)
        
        send_btn = tk.Button(
            button_frame,
            text="📤 Send",
            command=self.send_message,
            **button_style
        )
        send_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_chat,
            **button_style
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        help_btn = tk.Button(
            button_frame,
            text="❓ Help",
            command=self.show_help,
            **button_style
        )
        help_btn.pack(side=tk.LEFT, padx=5)
        
        exit_btn = tk.Button(
            button_frame,
            text="🚪 Exit",
            command=self.on_closing,
            bg="#f38ba8",
            fg="#1e1e2e",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8
        )
        exit_btn.pack(side=tk.RIGHT, padx=5)
        
        # Add hover effects
        for btn in [self.voice_btn, send_btn, clear_btn, help_btn]:
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.button_hover))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.button_color))
        
        exit_btn.bind("<Enter>", lambda e: exit_btn.config(bg="#eba0ac"))
        exit_btn.bind("<Leave>", lambda e: exit_btn.config(bg="#f38ba8"))
        
        # Status Bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            font=("Segoe UI", 9),
            bg=self.entry_bg,
            fg=self.fg_color,
            anchor=tk.W,
            padx=10,
            pady=5
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Display welcome message
        self.display_message("System", self.assistant.greet(), "system")
    
    def display_message(self, sender: str, message: str, tag: str = "assistant"):
        """Display a message in the chat"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        if sender == "User":
            self.chat_display.insert(tk.END, f"[{timestamp}] 👤 You: ", "user")
        elif sender == "System":
            self.chat_display.insert(tk.END, f"[{timestamp}] ⚙️  ", "system")
        else:
            assistant_name = self.assistant.config.get('assistant_name', 'Assistant')
            self.chat_display.insert(tk.END, f"[{timestamp}] 🤖 {assistant_name}: ", "assistant")
        
        self.chat_display.insert(tk.END, f"{message}\n\n", tag)
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def update_status(self, message: str):
        """Update the status bar"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
    
    def send_message(self):
        """Send a message to the assistant"""
        message = self.input_entry.get().strip()
        
        if not message:
            return
        
        # Display user message
        self.display_message("User", message, "user")
        self.input_entry.delete(0, tk.END)
        
        # Update status
        self.update_status("Processing...")
        
        # Process in thread to avoid blocking UI
        thread = threading.Thread(target=self._process_message, args=(message,), daemon=True)
        thread.start()
    
    def _process_message(self, message: str):
        """Process message in a separate thread"""
        try:
            response = self.assistant.process_command(message)
            
            if response == "exit":
                self.root.after(0, self.on_closing)
            elif response:
                self.root.after(0, self.display_message, "Assistant", response)
                # Speak in thread to avoid blocking
                if self.assistant.engine:
                    speak_thread = threading.Thread(
                        target=self.assistant.speak, 
                        args=(response, False), 
                        daemon=True
                    )
                    speak_thread.start()
            
            self.root.after(0, self.update_status, "Ready")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            self.root.after(0, self.display_message, "System", f"Error: {str(e)}", "system")
            self.root.after(0, self.update_status, "Error")
    
    def voice_input(self):
        """Handle voice input"""
        if self.listening:
            return
        
        self.listening = True
        self.voice_btn.config(text="⏸️ Listening...", state=tk.DISABLED)
        self.update_status("Listening for voice input...")
        
        # Run in thread
        thread = threading.Thread(target=self._voice_input_thread, daemon=True)
        thread.start()
    
    def _voice_input_thread(self):
        """Voice input in separate thread"""
        try:
            query = self.assistant.listen()
            
            if query:
                self.root.after(0, self.input_entry.delete, 0, tk.END)
                self.root.after(0, self.input_entry.insert, 0, query)
                self.root.after(0, self.send_message)
            else:
                self.root.after(0, self.display_message, "System", 
                              "Could not understand audio. Please try again.", "system")
        except Exception as e:
            logger.error(f"Voice input error: {e}")
            self.root.after(0, self.display_message, "System", 
                          f"Voice input error: {str(e)}", "system")
        finally:
            self.listening = False
            self.root.after(0, self.voice_btn.config, {"text": "🎤 Voice", "state": tk.NORMAL})
            self.root.after(0, self.update_status, "Ready")
    
    def clear_chat(self):
        """Clear the chat display"""
        if messagebox.askyesno("Clear Chat", "Are you sure you want to clear the chat history?"):
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.config(state=tk.DISABLED)
            self.assistant.conversation_history.clear()
            self.update_status("Chat cleared")
    
    def show_help(self):
        """Show help dialog"""
        help_text = self.assistant.get_help()
        messagebox.showinfo("Help - Available Commands", help_text)
    
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.assistant.running = False
            self.root.destroy()
    
    def run(self):
        """Start the GUI"""
        try:
            self.root.mainloop()
        except Exception as e:
            logger.error(f"GUI error: {e}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    print("This file should be imported by ai_assistant.py")
    print("Run: python ai_assistant.py")
