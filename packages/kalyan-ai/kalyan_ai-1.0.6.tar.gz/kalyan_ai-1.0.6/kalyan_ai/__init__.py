import subprocess
import time
import requests
import threading
import os
import signal
import atexit
from pathlib import Path
import sys
import platform
import shutil
import asyncio


class KalyanAI:
    def __init__(self, api_key="kalyan@ai"):
        self.api_key = api_key
        self.base_url = "http://localhost:8000/v1"
        self.server_process = None
        self.server_started = False
        self.ollama_installed = False
        
    def _check_ollama_installed(self):
        """Check if Ollama is installed"""
        try:
            result = subprocess.run(['ollama', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def _install_ollama(self):
        """Auto-install Ollama if not present"""
        print("🔧 Ollama not found. Installing automatically...")
        
        system = platform.system().lower()
        
        try:
            if system == "windows":
                print("📥 Downloading Ollama for Windows...")
                import urllib.request
                urllib.request.urlretrieve(
                    "https://ollama.com/download/OllamaSetup.exe", 
                    "OllamaSetup.exe"
                )
                print("⚠️  Please run OllamaSetup.exe manually and restart this script")
                return False
                
            elif system == "darwin":  # macOS
                subprocess.run(['curl', '-fsSL', 'https://ollama.com/install.sh'], 
                             check=True, shell=True)
                
            else:  # Linux
                subprocess.run(['curl', '-fsSL', 'https://ollama.com/install.sh', '|', 'sh'], 
                             check=True, shell=True)
            
            print("✅ Ollama installed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to install Ollama: {e}")
            print("Please install Ollama manually from https://ollama.com")
            return False
    
    def _ensure_ollama_model(self, model="llama3.1:8b"):
        """Ensure the model is downloaded"""
        try:
            
            result = subprocess.run(['ollama', 'list'], 
                                  capture_output=True, text=True, timeout=10)
            
            if model not in result.stdout:
                print(f"📥 Downloading model {model}... (This may take a while)")
                subprocess.run(['ollama', 'pull', model], check=True, timeout=300)
                print(f"✅ Model {model} downloaded successfully!")
            
                
            return True
            
        except subprocess.TimeoutExpired:
            print("❌ Model download timed out. Please try again.")
            return False
        except Exception as e:
            print(f"❌ Failed to download model: {e}")
            return False
    
    def _start_ollama_service(self):
        """Start Ollama service"""
        try:
            
            if platform.system().lower() == "windows":
                subprocess.Popen(['ollama', 'serve'], 
                               creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.Popen(['ollama', 'serve'], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
            
            # Wait for service to start
            for i in range(30):
                try:
                    requests.get("http://localhost:11434/api/tags", timeout=2)
                    
                    return True
                except:
                    time.sleep(1)
            
            print("❌ Failed to start Ollama service")
            return False
            
        except Exception as e:
            print(f"❌ Error starting Ollama: {e}")
            return False
    
    def _is_server_running(self):
        """Check if the API server is already running"""
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def _start_server(self):
        """Start the API server automatically"""
        if not self._is_server_running():
            pass
            
            # Get the api_server.py from package
            import kalyan_ai.api_server as api_server
            
            # Start the server in a separate thread
            def run_server():
                import uvicorn
                if platform.system().lower() == "windows":
                    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
                uvicorn.run(api_server.app, host="0.0.0.0", port=8000, log_level="critical")
            
            server_thread = threading.Thread(target=run_server, daemon=True)
            server_thread.start()
            
            # Wait for server to start
            
            for i in range(30):
                if self._is_server_running():
                    
                    self.server_started = True
                    return True
                time.sleep(1)
                if i % 5 == 0:
                    print(f"⏳ Still starting... ({i}s)")
            
            print("❌ Failed to start server within 30 seconds")
            return False
        else:
            print("✅ KalyanAI server already running!")
            self.server_started = True
            return True
    
    def _full_setup(self):
        """Complete setup process"""
        
        
        # Step 1: Check/Install Ollama
        if not self._check_ollama_installed():
            if not self._install_ollama():
                return False
        
        # Step 2: Start Ollama service
        if not self._start_ollama_service():
            return False
        
        # Step 3: Download model
        if not self._ensure_ollama_model():
            return False
        
        # Step 4: Start API server
        if not self._start_server():
            return False
        
        
        return True
    
    def _ensure_ready(self):
        """Ensure everything is ready"""
        if not self.server_started and not self._is_server_running():
            if not self._full_setup():
                raise Exception("Failed to setup KalyanAI. Please check the logs above.")
    
    def chat_completion(self, messages, model="llama3.1:8b", max_tokens=500, temperature=0.3, **kwargs):
        """OpenAI-style chat completion"""
        self._ensure_ready()
        
        try:
            import openai
        except ImportError:
            print("Installing OpenAI SDK...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'openai'])
            import openai
        
        client = openai.OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"API request failed: {str(e)}")
    
    def generate_content(self, prompt, **kwargs):
        """Gemini-style simple content generation"""
        messages = [{"role": "user", "content": prompt}]
        return self.chat_completion(messages, **kwargs)

# Global instance
_kalyan_ai_instance = None

def _get_instance():
    global _kalyan_ai_instance
    if _kalyan_ai_instance is None:
        _kalyan_ai_instance = KalyanAI()
    return _kalyan_ai_instance

def generate_content(prompt, max_tokens=500, temperature=0.3, **kwargs):
    """
    Generate content from a prompt - works like Gemini's generate_content()
    
    Example:
        from kalyan_ai import generate_content
        response = generate_content("What is machine learning?")
        print(response)
    """
    return _get_instance().generate_content(prompt, max_tokens=max_tokens, temperature=temperature, **kwargs)

def chat_completion(messages, model="llama3.1:8b", **kwargs):
    """
    OpenAI-style chat completion
    
    Example:
        from kalyan_ai import chat_completion
        messages = [{"role": "user", "content": "Hello!"}]
        response = chat_completion(messages)
        print(response)
    """
    return _get_instance().chat_completion(messages, model=model, **kwargs)

def configure(api_key="kalyan@ai"):
    """Configure the API key"""
    global _kalyan_ai_instance
    _kalyan_ai_instance = KalyanAI(api_key=api_key)

def check_status():
    """Check if KalyanAI is ready to use"""
    try:
        response = generate_content("Hi", max_tokens=10)
        print("✅ KalyanAI is working perfectly!")
        print(f"Test response: {response}")
        return True
    except Exception as e:
        print(f"❌ KalyanAI status check failed: {e}")
        return False

# Auto-setup on import
def quick_setup():
    """Quick setup function"""
    try:
        instance = _get_instance()
        instance._ensure_ready()
        print("🎉 KalyanAI is ready! Try: generate_content('Hello world')")
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        print("📖 Manual setup required. Please install Ollama from https://ollama.com")

if __name__ == "__main__":
    quick_setup()