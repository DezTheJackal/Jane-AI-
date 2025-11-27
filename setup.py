#!/usr/bin/env python3
"""
AI Assistant - Automated Setup Script (IMPROVED VERSION)
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

def run_command(command, description="Running command", capture_output=True):
    """Run a shell command and return success status"""
    try:
        print_colored(f"  → {description}...", Colors.BLUE)
        
        if capture_output:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
        else:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                timeout=300
            )
        
        print_colored(f"  ✓ Success!", Colors.GREEN)
        return True, None
    except subprocess.TimeoutExpired:
        print_colored(f"  ✗ Timeout: Command took too long", Colors.RED)
        return False, "Timeout"
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if capture_output and e.stderr else str(e)
        print_colored(f"  ✗ Error: {error_msg}", Colors.RED)
        return False, error_msg
    except Exception as e:
        print_colored(f"  ✗ Unexpected error: {e}", Colors.RED)
        return False, str(e)

def check_python_version():
    """Check if Python version is compatible"""
    print_header("🔍 Checking Python Version")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print_colored(f"✗ Python 3.7+ required. You have Python {version.major}.{version.minor}", Colors.RED)
        print_colored("\nPlease upgrade Python:", Colors.YELLOW)
        print_colored("  • Windows: Download from https://www.python.org/downloads/", Colors.YELLOW)
        print_colored("  • macOS: brew install python3", Colors.YELLOW)
        print_colored("  • Linux: sudo apt install python3 python3-pip", Colors.YELLOW)
        return False
    
    print_colored(f"✓ Python {version.major}.{version.minor}.{version.micro} detected", Colors.GREEN)
    return True

def check_pip():
    """Check if pip is available"""
    print_header("📦 Checking pip")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print_colored("✓ pip is available", Colors.GREEN)
        return True
    except:
        print_colored("✗ pip is not available", Colors.RED)
        print_colored("\nInstalling pip...", Colors.YELLOW)
        
        # Try to install pip
        success, _ = run_command(
            f"{sys.executable} -m ensurepip --default-pip",
            "Installing pip"
        )
        
        if not success:
            print_colored("\nManual pip installation required:", Colors.YELLOW)
            print_colored("  • Download: https://bootstrap.pypa.io/get-pip.py", Colors.YELLOW)
            print_colored("  • Run: python get-pip.py", Colors.YELLOW)
            return False
        
        return True

def install_pip_packages():
    """Install required Python packages"""
    print_header("📦 Installing Python Dependencies")
    
    packages = [
        "pyttsx3",
        "SpeechRecognition",
        "openai",
        "wikipedia",
        "requests"
    ]
    
    os_name = platform.system()
    
    # Upgrade pip first
    print_colored("\n🔄 Upgrading pip to latest version...", Colors.CYAN)
    run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "Upgrading pip"
    )
    
    # Special handling for PyAudio
    print_colored("\n🎤 Installing PyAudio (audio input/output)...", Colors.CYAN)
    pyaudio_installed = False
    
    if os_name == "Darwin":  # macOS
        print_colored("📱 macOS detected - Installing PortAudio first...", Colors.YELLOW)
        
        # Check if Homebrew is installed
        try:
            subprocess.run(["brew", "--version"], check=True, capture_output=True)
            success, _ = run_command("brew install portaudio", "Installing PortAudio via Homebrew")
            
            if success:
                success, _ = run_command(
                    f"{sys.executable} -m pip install pyaudio",
                    "Installing PyAudio"
                )
                pyaudio_installed = success
        except:
            print_colored("  ⚠ Homebrew not found. Please install Homebrew first:", Colors.YELLOW)
            print_colored("     /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"", Colors.YELLOW)
    
    elif os_name == "Linux":
        print_colored("🐧 Linux detected - Installing system dependencies...", Colors.YELLOW)
        
        # Try different package managers
        package_managers = [
            ("apt-get", "sudo apt-get update && sudo apt-get install -y python3-pyaudio portaudio19-dev python3-dev"),
            ("yum", "sudo yum install -y python3-pyaudio portaudio-devel python3-devel"),
            ("dnf", "sudo dnf install -y python3-pyaudio portaudio-devel python3-devel"),
            ("pacman", "sudo pacman -S --noconfirm python-pyaudio portaudio")
        ]
        
        for pm, cmd in package_managers:
            try:
                subprocess.run([pm, "--version"], check=True, capture_output=True)
                print_colored(f"  Found package manager: {pm}", Colors.GREEN)
                success, _ = run_command(cmd, f"Installing audio dependencies via {pm}", capture_output=False)
                
                if success:
                    success, _ = run_command(
                        f"{sys.executable} -m pip install pyaudio",
                        "Installing PyAudio"
                    )
                    pyaudio_installed = success
                    break
            except:
                continue
        
        if not pyaudio_installed:
            print_colored("  ⚠ Could not install PyAudio automatically", Colors.YELLOW)
            print_colored("    Try manually: sudo apt-get install python3-pyaudio", Colors.YELLOW)
    
    elif os_name == "Windows":
        print_colored("🪟 Windows detected - Using pipwin for PyAudio...", Colors.YELLOW)
        
        # Try pipwin first
        success, _ = run_command(
            f"{sys.executable} -m pip install pipwin",
            "Installing pipwin"
        )
        
        if success:
            success, _ = run_command(
                f"{sys.executable} -m pipwin install pyaudio",
                "Installing PyAudio via pipwin"
            )
            pyaudio_installed = success
        
        if not pyaudio_installed:
            print_colored("  ⚠ pipwin failed, trying direct installation...", Colors.YELLOW)
            success, _ = run_command(
                f"{sys.executable} -m pip install pyaudio",
                "Installing PyAudio"
            )
            pyaudio_installed = success
        
        if not pyaudio_installed:
            print_colored("  ⚠ PyAudio installation failed", Colors.YELLOW)
            print_colored("    Manual installation:", Colors.YELLOW)
            print_colored("    1. Download wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio", Colors.YELLOW)
            print_colored("    2. Run: pip install PyAudio‑0.2.11‑cp3X‑cp3Xm‑win_amd64.whl", Colors.YELLOW)
    
    # Install remaining packages
    print_colored("\n📚 Installing core packages...", Colors.CYAN)
    success_count = 0
    failed_packages = []
    
    for i, package in enumerate(packages, 1):
        print_colored(f"\n[{i}/{len(packages)}] Installing {package}...", Colors.CYAN)
        
        success, error = run_command(
            f"{sys.executable} -m pip install {package}",
            f"Installing {package}"
        )
        
        if success:
            success_count += 1
        else:
            failed_packages.append((package, error))
    
    # Summary
    print(f"\n{'='*70}")
    total_packages = len(packages) + (1 if pyaudio_installed else 0)
    installed = success_count + (1 if pyaudio_installed else 0)
    print_colored(f"✓ Successfully installed {installed}/{total_packages} packages", Colors.GREEN)
    
    if failed_packages:
        print_colored(f"\n⚠ Failed packages:", Colors.YELLOW)
        for pkg, error in failed_packages:
            print_colored(f"  • {pkg}: {error[:100]}", Colors.RED)
    
    if not pyaudio_installed:
        print_colored(f"\n⚠ PyAudio not installed - voice features will not work", Colors.YELLOW)
    
    return len(failed_packages) == 0 and pyaudio_installed

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
        try:
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
                created.append(str(path))
                print_colored(f"  ✓ Created: {path}", Colors.GREEN)
            else:
                print_colored(f"  ℹ Already exists: {path}", Colors.BLUE)
        except Exception as e:
            print_colored(f"  ✗ Failed to create {path}: {e}", Colors.RED)
    
    # Create README
    try:
        readme_path = directories["base"] / "README.txt"
        if not readme_path.exists():
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write("AI Assistant Directory Structure\n")
                f.write("================================\n\n")
                f.write("music/     - Place your music files here (MP3, WAV)\n")
                f.write("videos/    - Place your video files here (MP4, AVI)\n")
                f.write("documents/ - Place documents here\n")
                f.write("logs/      - Assistant logs are stored here\n")
                f.write("temp/      - Temporary files\n\n")
                f.write("Configuration file: ~/.ai_assistant_config.json\n")
                f.write("Main script: ai_assistant.py\n")
            print_colored(f"  ✓ Created README in {base_dir}", Colors.GREEN)
    except Exception as e:
        print_colored(f"  ⚠ Failed to create README: {e}", Colors.YELLOW)
    
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
        "model": "gpt-3.5-turbo",
        "max_history": 10,
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
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        print_colored(f"  ✓ Configuration file created: {config_path}", Colors.GREEN)
    except Exception as e:
        print_colored(f"  ✗ Failed to create config: {e}", Colors.RED)
        return None
    
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
            
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                config['openai_api_key'] = api_key
                
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2)
                
                print_colored("  ✓ OpenAI API key saved!", Colors.GREEN)
                return True
            except Exception as e:
                print_colored(f"  ✗ Failed to save API key: {e}", Colors.RED)
    
    print_colored("\n  ℹ You can configure OpenAI later by running:", Colors.YELLOW)
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
        print_colored("  Required files:", Colors.YELLOW)
        for file in required_files:
            print_colored(f"    • {file}", Colors.YELLOW)
        return False
    
    return True

def create_launcher_scripts(directories):
    """Create launcher scripts for easy access"""
    print_header("🚀 Creating Launcher Scripts")
    
    base_dir = directories["base"]
    current_dir = Path.cwd()
    python_exec = sys.executable
    
    try:
        # Windows batch file
        if platform.system() == "Windows":
            bat_content = f"""@echo off
cd /d "{current_dir}"
"{python_exec}" ai_assistant.py
pause
"""
            bat_path = base_dir / "Launch_Assistant.bat"
            with open(bat_path, 'w') as f:
                f.write(bat_content)
            print_colored(f"  ✓ Created: Launch_Assistant.bat", Colors.GREEN)
            
            # Terminal mode batch
            bat_terminal = f"""@echo off
cd /d "{current_dir}"
"{python_exec}" ai_assistant.py --terminal
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
"{python_exec}" ai_assistant.py
"""
            sh_path = base_dir / "launch_assistant.sh"
            with open(sh_path, 'w') as f:
                f.write(sh_content)
            os.chmod(sh_path, 0o755)
            print_colored(f"  ✓ Created: launch_assistant.sh", Colors.GREEN)
            
            # Terminal mode script
            sh_terminal = f"""#!/bin/bash
cd "{current_dir}"
"{python_exec}" ai_assistant.py --terminal
"""
            sh_term_path = base_dir / "launch_assistant_terminal.sh"
            with open(sh_term_path, 'w') as f:
                f.write(sh_terminal)
            os.chmod(sh_term_path, 0o755)
            print_colored(f"  ✓ Created: launch_assistant_terminal.sh", Colors.GREEN)
    except Exception as e:
        print_colored(f"  ⚠ Failed to create launcher scripts: {e}", Colors.YELLOW)

def test_installation():
    """Test if installation was successful"""
    print_header("🧪 Testing Installation")
    
    tests = [
        ("pyttsx3", "Text-to-Speech"),
        ("speech_recognition", "Speech Recognition"),
        ("openai", "OpenAI API"),
        ("wikipedia", "Wikipedia"),
        ("requests", "Requests")
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
        failed.append("PyAudio (optional)")
    
    print(f"\n{passed}/{len(tests) + 1} tests passed")
    
    return len(failed) == 0 or "PyAudio (optional)" in failed

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
    print("  • If PyAudio installation failed, see BUG_FIXES_AND_IMPROVEMENTS.md")
    print("  • For issues, check logs in: " + str(directories['logs']))
    print("  • Run in terminal mode first to test: python ai_assistant.py --terminal")
    
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
    ║                       IMPROVED VERSION                        ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """, Colors.CYAN + Colors.BOLD)
    
    print_colored("This script will:", Colors.BOLD)
    print("  ✓ Check Python version and pip")
    print("  ✓ Install all required dependencies")
    print("  ✓ Create directory structure")
    print("  ✓ Configure the assistant")
    print("  ✓ Create launcher scripts")
    print("  ✓ Test the installation\n")
    
    proceed = input("Do you want to proceed? (Y/n): ").strip().lower()
    if proceed == 'n':
        print_colored("\nSetup cancelled.", Colors.YELLOW)
        return
    
    total_steps = 8
    current_step = 0
    
    # Step 1: Check Python
    current_step += 1
    print_step(current_step, total_steps, "Checking Python Version")
    if not check_python_version():
        print_colored("\n✗ Setup failed: Incompatible Python version", Colors.RED)
        return
    
    # Step 2: Check pip
    current_step += 1
    print_step(current_step, total_steps, "Checking pip")
    if not check_pip():
        print_colored("\n✗ Setup failed: pip not available", Colors.RED)
        return
    
    # Step 3: Check files
    current_step += 1
    print_step(current_step, total_steps, "Verifying Assistant Files")
    if not download_assistant_files():
        print_colored("\n⚠ Setup incomplete: Missing required files", Colors.YELLOW)
        print_colored("Please download the fixed files and try again.", Colors.YELLOW)
        return
    
    # Step 4: Install packages
    current_step += 1
    print_step(current_step, total_steps, "Installing Dependencies")
    packages_ok = install_pip_packages()
    
    if not packages_ok:
        print_colored("\n⚠ Some packages failed to install", Colors.YELLOW)
        continue_setup = input("Continue with setup anyway? (y/N): ").strip().lower()
        if continue_setup != 'y':
            print_colored("\nSetup cancelled.", Colors.YELLOW)
            return
    
    # Step 5: Create directories
    current_step += 1
    print_step(current_step, total_steps, "Creating Directory Structure")
    directories = create_directory_structure()
    
    # Step 6: Create config
    current_step += 1
    print_step(current_step, total_steps, "Creating Configuration")
    create_config_file(directories)
    
    # Step 7: Configure OpenAI
    current_step += 1
    print_step(current_step, total_steps, "OpenAI Setup")
    configure_openai_api()
    
    # Step 8: Create launchers
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
        import traceback
        traceback.print_exc()
        sys.exit(1)
