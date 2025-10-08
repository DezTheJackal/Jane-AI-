#!/usr/bin/env python3
"""
AI Assistant - Automated Setup Script
Installs dependencies, creates directories, and configures the assistant
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path
import urllib.request
import shutil

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_colored(text, color=Colors.GREEN):
    """Print colored text"""
    print(f"{color}{text}{Colors.END}")

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print_colored(f"  {text}", Colors.HEADER + Colors.BOLD)
    print("="*70 + "\n")

def print_step(step_num, total_steps, description):
    """Print a step in the installation process"""
    print_colored(f"[{step_num}/{total_steps}] {description}", Colors.CYAN)

def run_command(command, description="Running command"):
    """Run a shell command and return success status"""
    try:
        print_colored(f"  → {description}...", Colors.BLUE)
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print_colored(f"  ✓ Success!", Colors.GREEN)
        return True
    except subprocess.CalledProcessError as e:
        print_colored(f"  ✗ Error: {e.stderr}", Colors.RED)
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print_header("🔍 Checking Python Version")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print_colored(f"✗ Python 3.7+ required. You have Python {version.major}.{version.minor}", Colors.RED)
        return False
    
    print_colored(f"✓ Python {version.major}.{version.minor}.{version.micro} detected", Colors.GREEN)
    return True

def install_pip_packages():
    """Install required Python packages"""
    print_header("📦 Installing Python Dependencies")
    
    packages = [
        "pyttsx3",
        "SpeechRecognition",
        "pyaudio",
        "openai",
        "wikipedia",
        "requests"
    ]
    
    os_name = platform.system()
    
    # Special handling for PyAudio
    if os_name == "Darwin":  # macOS
        print_colored("📱 macOS detected - Installing PortAudio first...", Colors.YELLOW)
        run_command("brew install portaudio", "Installing PortAudio via Homebrew")
    elif os_name == "Linux":
        print_colored("🐧 Linux detected - Installing system dependencies...", Colors.YELLOW)
        distro_commands = [
            "sudo apt-get update && sudo apt-get install -y python3-pyaudio portaudio19-dev",
            "sudo yum install -y python3-pyaudio portaudio-devel",
            "sudo pacman -S python-pyaudio portaudio"
        ]
        for cmd in distro_commands:
            if run_command(cmd, "Installing system audio libraries"):
                break
    elif os_name == "Windows":
        print_colored("🪟 Windows detected - PyAudio may require additional setup", Colors.YELLOW)
        print_colored("   If PyAudio fails, try: pip install pipwin && pipwin install pyaudio", Colors.YELLOW)
    
    # Install packages
    success_count = 0
    failed_packages = []
    
    for i, package in enumerate(packages, 1):
        print_colored(f"\n[{i}/{len(packages)}] Installing {package}...", Colors.CYAN)
        
        if package == "pyaudio" and os_name == "Windows":
            # Try pipwin first on Windows
            if run_command("pip install pipwin", "Installing pipwin"):
                if run_command(f"pipwin install {package}", f"Installing {package} via pipwin"):
                    success_count += 1
                    continue
        
        if run_command(f"pip install {package}", f"Installing {package}"):
            success_count += 1
        else:
            failed_packages.append(package)
    
    print(f"\n✓ Successfully installed {success_count}/{len(packages)} packages")
    
    if failed_packages:
        print_colored(f"\n⚠ Failed to install: {', '.join(failed_packages)}", Colors.YELLOW)
        print_colored("  You may need to install these manually.", Colors.YELLOW)
    
    return len(failed_packages) == 0

def create_directory_structure():
    """Create necessary directories"""
    print_header("📁 Creating Directory Structure")
    
    home = Path.home()
    base_dir = home / "AIAssistant"
    
    directories = {
        "base": base_dir,
        "music": base_dir / "music",
        "videos": base_dir / "videos",
        "documents": base_dir / "documents",
        "logs": base_dir / "logs",
        "temp": base_dir / "temp"
    }
    
    created = []
    for name, path in directories.items():
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            created.append(str(path))
            print_colored(f"  ✓ Created: {path}", Colors.GREEN)
        else:
            print_colored(f"  ℹ Already exists: {path}", Colors.BLUE)
    
    # Create sample files
    readme_path = directories["base"] / "README.txt"
    if not readme_path.exists():
        with open(readme_path, 'w') as f:
            f.write("AI Assistant Directory Structure\n")
            f.write("================================\n\n")
            f.write("music/     - Place your music files here\n")
            f.write("videos/    - Place your video files here\n")
            f.write("documents/ - Place documents here\n")
            f.write("logs/      - Assistant logs are stored here\n")
            f.write("temp/      - Temporary files\n")
        print_colored(f"  ✓ Created README in {base_dir}", Colors.GREEN)
    
    return directories

def create_config_file(directories):
    """Create default configuration file"""
    print_header("⚙️ Creating Configuration File")
    
    config_path = Path.home() / ".ai_assistant_config.json"
    
    if config_path.exists():
        print_colored("  ℹ Configuration file already exists", Colors.YELLOW)
        overwrite = input("  Do you want to overwrite it? (y/N): ").strip().lower()
        if overwrite != 'y':
            print_colored("  ℹ Keeping existing configuration", Colors.BLUE)
            return config_path
    
    config = {
        "voice_rate": 175,
        "voice_volume": 0.9,
        "voice_index": 1,
        "openai_api_key": "",
        "assistant_name": "Assistant",
        "directories": {
            "base": str(directories["base"]),
            "music": str(directories["music"]),
            "videos": str(directories["videos"]),
            "documents": str(directories["documents"]),
            "logs": str(directories["logs"])
        },
        "preferences": {
            "auto_listen": False,
            "verbose_mode": True,
            "save_logs": True
        }
    }
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print_colored(f"  ✓ Configuration file created: {config_path}", Colors.GREEN)
    return config_path

def configure_openai_api():
    """Configure OpenAI API key"""
    print_header("🔑 OpenAI Configuration (Optional)")
    
    print_colored("The assistant can use OpenAI's GPT for advanced conversations.", Colors.BLUE)
    print_colored("Get your API key from: https://platform.openai.com/api-keys\n", Colors.BLUE)
    
    setup_openai = input("Do you want to configure OpenAI now? (y/N): ").strip().lower()
    
    if setup_openai == 'y':
        api_key = input("Enter your OpenAI API key: ").strip()
        
        if api_key:
            config_path = Path.home() / ".ai_assistant_config.json"
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            config['openai_api_key'] = api_key
            
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            print_colored("  ✓ OpenAI API key saved!", Colors.GREEN)
            return True
    
    print_colored("  ℹ You can configure OpenAI later by running:", Colors.YELLOW)
    print_colored("     python ai_assistant.py --config", Colors.YELLOW)
    return False

def download_assistant_files():
    """Download or verify assistant files"""
    print_header("📥 Checking Assistant Files")
    
    required_files = [
        "ai_assistant.py",
        "ai_assistant_gui.py"
    ]
    
    current_dir = Path.cwd()
    missing_files = []
    
    for file in required_files:
        file_path = current_dir / file
        if file_path.exists():
            print_colored(f"  ✓ Found: {file}", Colors.GREEN)
        else:
            print_colored(f"  ✗ Missing: {file}", Colors.RED)
            missing_files.append(file)
    
    if missing_files:
        print_colored(f"\n⚠ Missing files: {', '.join(missing_files)}", Colors.YELLOW)
        print_colored("  Please ensure all assistant files are in the current directory.", Colors.YELLOW)
        return False
    
    return True

def create_launcher_scripts(directories):
    """Create launcher scripts for easy access"""
    print_header("🚀 Creating Launcher Scripts")
    
    base_dir = directories["base"]
    current_dir = Path.cwd()
    
    # Windows batch file
    if platform.system() == "Windows":
        bat_content = f"""@echo off
cd /d "{current_dir}"
python ai_assistant.py
pause
"""
        bat_path = base_dir / "Launch_Assistant.bat"
        with open(bat_path, 'w') as f:
            f.write(bat_content)
        print_colored(f"  ✓ Created: Launch_Assistant.bat", Colors.GREEN)
        
        # Terminal mode batch
        bat_terminal = f"""@echo off
cd /d "{current_dir}"
python ai_assistant.py --terminal
pause
"""
        bat_term_path = base_dir / "Launch_Assistant_Terminal.bat"
        with open(bat_term_path, 'w') as f:
            f.write(bat_terminal)
        print_colored(f"  ✓ Created: Launch_Assistant_Terminal.bat", Colors.GREEN)
    
    # Unix shell script
    else:
        sh_content = f"""#!/bin/bash
cd "{current_dir}"
python3 ai_assistant.py
"""
        sh_path = base_dir / "launch_assistant.sh"
        with open(sh_path, 'w') as f:
            f.write(sh_content)
        os.chmod(sh_path, 0o755)
        print_colored(f"  ✓ Created: launch_assistant.sh", Colors.GREEN)
        
        # Terminal mode script
        sh_terminal = f"""#!/bin/bash
cd "{current_dir}"
python3 ai_assistant.py --terminal
"""
        sh_term_path = base_dir / "launch_assistant_terminal.sh"
        with open(sh_term_path, 'w') as f:
            f.write(sh_terminal)
        os.chmod(sh_term_path, 0o755)
        print_colored(f"  ✓ Created: launch_assistant_terminal.sh", Colors.GREEN)

def test_installation():
    """Test if installation was successful"""
    print_header("🧪 Testing Installation")
    
    tests = [
        ("pyttsx3", "Text-to-Speech"),
        ("speech_recognition", "Speech Recognition"),
        ("openai", "OpenAI API"),
    ]
    
    passed = 0
    failed = []
    
    for module, name in tests:
        try:
            __import__(module)
            print_colored(f"  ✓ {name} - OK", Colors.GREEN)
            passed += 1
        except ImportError:
            print_colored(f"  ✗ {name} - Failed", Colors.RED)
            failed.append(name)
    
    # Test PyAudio separately
    try:
        import pyaudio
        print_colored(f"  ✓ Audio Input (PyAudio) - OK", Colors.GREEN)
        passed += 1
    except ImportError:
        print_colored(f"  ⚠ Audio Input (PyAudio) - Not installed", Colors.YELLOW)
        print_colored(f"    Voice input will not work without PyAudio", Colors.YELLOW)
        failed.append("PyAudio")
    
    print(f"\n{passed}/{len(tests) + 1} tests passed")
    
    return len(failed) == 0

def print_final_instructions(directories):
    """Print final setup instructions"""
    print_header("🎉 Setup Complete!")
    
    print_colored("Installation Directory:", Colors.BOLD)
    print(f"  {directories['base']}\n")
    
    print_colored("To start the assistant:", Colors.BOLD)
    print_colored("  • GUI Mode (recommended):", Colors.GREEN)
    print(f"    python ai_assistant.py")
    print_colored("\n  • Terminal Mode:", Colors.GREEN)
    print(f"    python ai_assistant.py --terminal")
    
    print_colored("\nConfiguration:", Colors.BOLD)
    config_path = Path.home() / ".ai_assistant_config.json"
    print(f"  Config file: {config_path}")
    print(f"  To reconfigure: python ai_assistant.py --config")
    
    print_colored("\nQuick Tips:", Colors.BOLD)
    print("  1. Test your microphone before using voice commands")
    print("  2. For better accuracy, speak clearly and avoid background noise")
    print("  3. Configure OpenAI API for advanced AI conversations")
    print("  4. Check the README.md for detailed usage instructions")
    
    print_colored("\nTroubleshooting:", Colors.BOLD)
    print("  • If voice recognition fails, check microphone permissions")
    print("  • If PyAudio installation failed, see README for manual installation")
    print("  • For issues, check logs in: " + str(directories['logs']))
    
    print("\n" + "="*70)
    print_colored("  Ready to use! Run: python ai_assistant.py", Colors.GREEN + Colors.BOLD)
    print("="*70 + "\n")

def main():
    """Main setup process"""
    print_colored("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║           🤖 AI ASSISTANT - AUTOMATED SETUP 🤖               ║
    ║                                                               ║
    ║              One-Click Installation & Configuration           ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """, Colors.CYAN + Colors.BOLD)
    
    print_colored("This script will:", Colors.BOLD)
    print("  ✓ Check Python version")
    print("  ✓ Install all required dependencies")
    print("  ✓ Create directory structure")
    print("  ✓ Configure the assistant")
    print("  ✓ Create launcher scripts")
    print("  ✓ Test the installation\n")
    
    proceed = input("Do you want to proceed? (Y/n): ").strip().lower()
    if proceed == 'n':
        print_colored("\nSetup cancelled.", Colors.YELLOW)
        return
    
    total_steps = 7
    current_step = 0
    
    # Step 1: Check Python
    current_step += 1
    print_step(current_step, total_steps, "Checking Python Version")
    if not check_python_version():
        print_colored("\n✗ Setup failed: Incompatible Python version", Colors.RED)
        return
    
    # Step 2: Check files
    current_step += 1
    print_step(current_step, total_steps, "Verifying Assistant Files")
    if not download_assistant_files():
        print_colored("\n✗ Setup incomplete: Missing required files", Colors.RED)
        return
    
    # Step 3: Install packages
    current_step += 1
    print_step(current_step, total_steps, "Installing Dependencies")
    install_pip_packages()
    
    # Step 4: Create directories
    current_step += 1
    print_step(current_step, total_steps, "Creating Directory Structure")
    directories = create_directory_structure()
    
    # Step 5: Create config
    current_step += 1
    print_step(current_step, total_steps, "Creating Configuration")
    create_config_file(directories)
    
    # Step 6: Configure OpenAI
    current_step += 1
    print_step(current_step, total_steps, "OpenAI Setup")
    configure_openai_api()
    
    # Step 7: Create launchers
    current_step += 1
    print_step(current_step, total_steps, "Creating Launcher Scripts")
    create_launcher_scripts(directories)
    
    # Test installation
    test_installation()
    
    # Final instructions
    print_final_instructions(directories)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\n✗ Setup interrupted by user", Colors.YELLOW)
        sys.exit(1)
    except Exception as e:
        print_colored(f"\n✗ Setup failed with error: {e}", Colors.RED)
        sys.exit(1)
