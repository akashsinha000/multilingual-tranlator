#!/usr/bin/env python3
"""
Startup script for the Multilingual Translator application
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import flask
        import transformers
        import torch
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        print("Creating .env file...")
        with open(env_file, "w") as f:
            f.write("""# Flask Configuration
FLASK_ENV=development
PORT=5000

# Hugging Face Configuration (optional)
# HF_TOKEN=your_huggingface_token_here

# Application Configuration
MAX_TEXT_LENGTH=1000
CACHE_MODELS=true
LOG_LEVEL=INFO
""")
        print("✅ Created .env file")
    else:
        print("✅ .env file already exists")

def main():
    """Main startup function"""
    print("🚀 Starting Multilingual Translator Application")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Create .env file if needed
    create_env_file()
    
    # Set environment variables
    os.environ.setdefault('FLASK_ENV', 'development')
    os.environ.setdefault('PORT', '5000')
    
    print("\n📱 Application Features:")
    print("• Real-time translation across 20+ languages")
    print("• Mobile-friendly responsive interface")
    print("• Auto-translate functionality")
    print("• Text-to-speech support")
    print("• PWA capabilities")
    print("• REST API endpoints")
    
    print(f"\n🌐 Starting server on http://localhost:{os.environ.get('PORT', 5000)}")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Import and run the app
    try:
        from app import app
        app.run(
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000)),
            debug=os.environ.get('FLASK_ENV') == 'development'
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
