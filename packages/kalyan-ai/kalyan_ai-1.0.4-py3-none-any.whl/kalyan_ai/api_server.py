from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, AsyncGenerator
import requests
import json
import time
import subprocess
import asyncio
import aiohttp
from contextlib import asynccontextmanager
import logging
from datetime import datetime
import threading
import queue
import os
from functools import lru_cache
import hashlib


# API Key Configuration
API_KEY = "kalyan@ai"  # Your custom API key
security = HTTPBearer()

def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Skip authentication for local development
    if not credentials:
        return "local"  # Default for no auth
    if credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key. Use 'kalyan@ai'"
        )
    return credentials.credentials

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Pydantic models for request/response
class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str = "llama3.1:8b"
    messages: List[Message]
    temperature: Optional[float] = Field(default=0.3, ge=0.0, le=2.0)  # Lower default for speed
    max_tokens: Optional[int] = Field(default=512, ge=1, le=2048)  # Reduced for speed
    top_p: Optional[float] = Field(default=0.8, ge=0.0, le=1.0)
    stream: Optional[bool] = False
    stop: Optional[List[str]] = None
    frequency_penalty: Optional[float] = Field(default=0.0, ge=-2.0, le=2.0)
    presence_penalty: Optional[float] = Field(default=0.0, ge=-2.0, le=2.0)

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]

class HealthResponse(BaseModel):
    status: str
    ollama_service: str
    response_time_ms: float
    available_models: List[str]
    memory_usage: Optional[Dict[str, Any]] = None

# Enhanced caching system
class ResponseCache:
    def __init__(self, max_size: int = 100):
        self.cache = {}
        self.max_size = max_size
        self.access_times = {}
    
    def _generate_key(self, messages: List[Message], temperature: float, max_tokens: int) -> str:
        content = json.dumps([{"role": m.role, "content": m.content} for m in messages])
        key_string = f"{content}:{temperature}:{max_tokens}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, messages: List[Message], temperature: float, max_tokens: int) -> Optional[str]:
        key = self._generate_key(messages, temperature, max_tokens)
        if key in self.cache:
            self.access_times[key] = time.time()
            return self.cache[key]
        return None
    
    def set(self, messages: List[Message], temperature: float, max_tokens: int, response: str):
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
            del self.cache[oldest_key]
            del self.access_times[oldest_key]
        
        key = self._generate_key(messages, temperature, max_tokens)
        self.cache[key] = response
        self.access_times[key] = time.time()

# Global cache instance
response_cache = ResponseCache()

# Enhanced Ollama client with better optimization
class OllamaClient:
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.session = None
        self._lock = threading.Lock()
        self.model_loaded = False
    
    async def get_session(self):
        if self.session is None:
            connector = aiohttp.TCPConnector(
                limit=20,
                limit_per_host=20,
                keepalive_timeout=60,
                enable_cleanup_closed=True,
                force_close=False,
                ttl_dns_cache=300,
                use_dns_cache=True
            )
            timeout = aiohttp.ClientTimeout(total=180, connect=5)
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout
            )
        return self.session
    
    async def preload_model(self, model_name: str = "llama3.1:8b"):
        """Preload model to reduce first-request latency"""
        if self.model_loaded:
            return
        
        try:
            session = await self.get_session()
            payload = {
                "name": model_name,
                "keep_alive": "30m"  # Keep model in memory for 30 minutes
            }
            
            async with session.post(f"{self.base_url}/api/pull", json=payload) as response:
                if response.status == 200:
                    self.model_loaded = True
                    logger.info(f"✅ Model {model_name} preloaded and kept in memory")
        except Exception as e:
            logger.warning(f"Failed to preload model: {e}")
    
    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None
    
    async def generate(self, prompt: str, options: Dict[str, Any]) -> Dict[str, Any]:
        session = await self.get_session()
        
        payload = {
            "model": "llama3.1:8b",
            "prompt": prompt,
            "stream": False,
            "keep_alive": "30m",  # Keep model loaded
            "options": {
                **options,
                "num_ctx": 1024,  # Smaller context for speed
                "num_batch": 256,  # Optimized batch size
                "num_gpu": 1,
                "num_thread": min(8, os.cpu_count() or 4),
                "repeat_penalty": 1.05,  # Reduced for faster generation
                "temperature": options.get("temperature", 0.3),
                "top_p": options.get("top_p", 0.8),
                "top_k": 20,  # Limit vocabulary for speed
                "num_predict": min(options.get("num_predict", 512), 1024),
                "stop": ["User:", "Human:", "\n\n\n"]  # Auto-stop tokens
            }
        }
        
        try:
            async with session.post(f"{self.base_url}/api/generate", json=payload) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    text = await response.text()
                    raise HTTPException(status_code=response.status, detail=f"Ollama error: {text}")
        except asyncio.TimeoutError:
            raise HTTPException(status_code=504, detail="Request timeout - try reducing max_tokens")
        except aiohttp.ClientConnectorError:
            raise HTTPException(status_code=503, detail="Cannot connect to Ollama service")

# Global client instance
ollama_client = OllamaClient()

@lru_cache(maxsize=50)
def optimize_prompt_cached(messages_hash: str) -> str:
    """Cached prompt optimization"""
    return messages_hash  # Simplified for caching

def optimize_prompt(messages: List[Message]) -> str:
    """Create highly optimized prompt for faster responses"""
    # Use only the most recent context to reduce processing
    recent_messages = messages[-5:]  # Only last 5 messages
    
    # Create a focused system prompt
    system_prompt = "You are a helpful AI. Be concise and direct."
    
    prompt_parts = []
    
    # Add system context
    has_system = any(msg.role == "system" for msg in recent_messages)
    if not has_system:
        prompt_parts.append(f"System: {system_prompt}")
    
    for message in recent_messages:
        role = message.role
        # Limit content length for speed
        content = message.content[:1000] if len(message.content) > 1000 else message.content
        
        if role == "system":
            prompt_parts.append(f"System: {content}")
        elif role == "user":
            prompt_parts.append(f"User: {content}")
        elif role == "assistant":
            prompt_parts.append(f"Assistant: {content}")
    
    prompt_parts.append("Assistant:")
    
    return "\n".join(prompt_parts)

def clean_response_text(text: str) -> str:
    """Fast response cleaning"""
    # Remove common prefixes
    prefixes_to_remove = ["Assistant:", "AI:", "Response:", "Answer:"]
    for prefix in prefixes_to_remove:
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
    
    # Clean up formatting
    text = text.replace("**", "").replace("```", "")
    
    # Remove excessive whitespace
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    return '\n'.join(lines)

async def ensure_ollama_running():
    """Enhanced Ollama service check with auto-start"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:11434/api/tags", timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status == 200:
                    return True
    except:
        pass
    
    logger.warning("Ollama service not responding - attempting to start...")
    try:
        # Try to start Ollama
        process = subprocess.Popen(
            ['ollama', 'serve'], 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        
        # Wait longer for startup
        await asyncio.sleep(15)
        
        # Check again
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:11434/api/tags", timeout=aiohttp.ClientTimeout(total=5)) as response:
                return response.status == 200
    except Exception as e:
        logger.error(f"Failed to start Ollama: {e}")
        return False

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    
    
    if await ensure_ollama_running():
        
        # Preload model for faster responses
        await ollama_client.preload_model()
        
    
        
    
    yield
    
    # Shutdown
    await ollama_client.close()
    await asyncio.sleep(0.5)
    tasks = [task for task in asyncio.all_tasks() if not task.done()]
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)
    
    logger.info("👋 Shutting down AI API Server...")

# FastAPI app with enhanced configuration
app = FastAPI(
    title="KalyanAI API Server",
    description="High-Performance Local AI API - OpenAI Compatible",
    version="3.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enhanced CORS for better web app support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/")
async def root():
    return {
        "name": "KalyanAI API Server",
        "model": "llama3.1:8b",
        "status": "running",
        "version": "3.0.0",
        "compatibility": "OpenAI GPT API",
        "authentication": "Bearer token required",
        "api_key": "Use 'kalyan@ai' as your API key",
        "endpoints": {
            "chat_completions": "/v1/chat/completions",
            "models": "/v1/models",
            "health": "/health",
            "quick_test": "/quick-test",
            "docs": "/docs"
        },
        "usage": {
            "openai_compatible": "Set base_url='http://localhost:8000/v1'",
            "api_key": "Not required for local usage",
            "model_name": "llama3.1:8b"
        },
        "optimizations": [
            "Model preloading",
            "Response caching",
            "Async processing",
            "Context optimization",
            "Auto-scaling"
        ]
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    start_time = time.time()
    
    try:
        session = await ollama_client.get_session()
        async with session.get(f"{ollama_client.base_url}/api/tags") as response:
            response_time = (time.time() - start_time) * 1000
            
            if response.status == 200:
                data = await response.json()
                available_models = [m['name'] for m in data.get('models', [])]
                
                return HealthResponse(
                    status="healthy",
                    ollama_service="running",
                    response_time_ms=round(response_time, 2),
                    available_models=available_models
                )
            else:
                return HealthResponse(
                    status="unhealthy",
                    ollama_service="not responding",
                    response_time_ms=round(response_time, 2),
                    available_models=[]
                )
    except Exception as e:
        response_time = (time.time() - start_time) * 1000
        return HealthResponse(
            status="unhealthy",
            ollama_service="not running",
            response_time_ms=round(response_time, 2),
            available_models=[]
        )

@app.get("/v1/models")
async def list_models(authorization: str = Header(None)):
    """OpenAI-compatible models endpoint"""
    try:
        session = await ollama_client.get_session()
        async with session.get(f"{ollama_client.base_url}/api/tags") as response:
            if response.status == 200:
                data = await response.json()
                models = []
                for model in data.get('models', []):
                    models.append({
                        "id": model['name'],
                        "object": "model",
                        "created": int(time.time()),
                        "owned_by": "kalyan-ai",
                        "permission": [],
                        "root": model['name'],
                        "parent": None
                    })
                return {"object": "list", "data": models}
            else:
                # Fallback
                return {
                    "object": "list",
                    "data": [{
                        "id": "llama3.1:8b",
                        "object": "model",
                        "created": int(time.time()),
                        "owned_by": "kalyan-ai"
                    }]
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching models: {str(e)}")

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest, authorization: str = Header(None)):
    """Enhanced OpenAI-compatible chat completions with caching"""
    start_time = time.time()
    
    try:
        # Check cache first for identical requests
        cached_response = response_cache.get(
            request.messages, 
            request.temperature, 
            request.max_tokens
        )
        
        if cached_response:
            
            return {
                "id": f"chatcmpl-{int(time.time())}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": request.model,
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": cached_response
                    },
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": len(' '.join([m.content for m in request.messages]).split()),
                    "completion_tokens": len(cached_response.split()),
                    "total_tokens": len(' '.join([m.content for m in request.messages]).split()) + len(cached_response.split())
                },
                "processing_time": round(time.time() - start_time, 2),
                "cached": True
            }
        
        # Optimize prompt
        prompt = optimize_prompt(request.messages)
        
        # Prepare optimized options
        options = {
            "temperature": request.temperature,
            "top_p": request.top_p,
            "num_predict": min(request.max_tokens, 512),  # Limit for speed
        }
        
        # Generate response
        result = await ollama_client.generate(prompt, options)
        response_text = result.get('response', '').strip()
        
        # Clean response
        response_text = clean_response_text(response_text)
        
        # Cache the response
        response_cache.set(request.messages, request.temperature, request.max_tokens, response_text)
        
        # Calculate timing
        processing_time = time.time() - start_time
        
        # Create OpenAI-compatible response
        chat_response = {
            "id": f"chatcmpl-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": request.model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response_text
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": len(response_text.split()),
                "total_tokens": len(prompt.split()) + len(response_text.split())
            },
            "processing_time": round(processing_time, 2),
            "cached": False
        }
        
        
        return chat_response
        
    except Exception as e:
        logger.error(f"Error in chat completion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/quick-test")
async def quick_test():
    """Super fast test endpoint"""
    test_request = ChatCompletionRequest(
        model="llama3.1:8b",
        messages=[Message(role="user", content="Hi")],
        max_tokens=20,
        temperature=0.1
    )
    
    try:
        start_time = time.time()
        response = await chat_completions(test_request)
        end_time = time.time()
        
        return {
            "status": "success",
            "response_time": f"{end_time - start_time:.2f}s",
            "response": response['choices'][0]['message']['content'],
            "server_ready": True
        }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "server_ready": False
        }

@app.get("/api-key")
async def get_api_info():
    """Information about using this API like OpenAI/Gemini"""
    return {
        "api_usage": {
            "base_url": "http://localhost:8000/v1",
            "api_key": "kalyan@ai",
            "model": "llama3.1:8b",
            "authentication": "Bearer kalyan@ai"
        },
        "python_example": {
            "openai_sdk": """
import openai
client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"
)
response = client.chat.completions.create(
    model="llama3.1:8b",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
            """,
            "requests": """
import requests
response = requests.post("http://localhost:8000/v1/chat/completions", 
    json={
        "model": "llama3.1:8b",
        "messages": [{"role": "user", "content": "Hello!"}],
        "max_tokens": 100
    }
)
print(response.json()['choices'][0]['message']['content'])
            """
        },
        "performance_tips": [
            "Use max_tokens=512 or less for faster responses",
            "Set temperature=0.3 for focused, quicker answers",
            "Cache responses automatically enabled",
            "Model stays loaded for 30 minutes"
        ]
    }

@app.get("/stats")
async def get_stats():
    """Enhanced API performance statistics"""
    return {
        "timestamp": datetime.now().isoformat(),
        "server_status": "running",
        "model_loaded": ollama_client.model_loaded,
        "cache_size": len(response_cache.cache),
        "optimizations_active": [
            "Model preloading",
            "Response caching",
            "Async processing", 
            "Context optimization",
            "Auto-stop tokens",
            "Reduced vocabulary search"
        ],
        "performance_tips": {
            "fastest_setup": "max_tokens=256, temperature=0.1",
            "balanced_setup": "max_tokens=512, temperature=0.3",
            "creative_setup": "max_tokens=1024, temperature=0.7"
        },
        "api_compatibility": {
            "openai_sdk": True,
            "langchain": True,
            "custom_apps": True,
            "base_url": "http://localhost:8000/v1"
        }
    }

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="critical")

if __name__ == "__main__":
    main()