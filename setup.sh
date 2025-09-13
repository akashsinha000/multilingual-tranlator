#!/bin/bash

# Multilingual Translator Setup Script
echo "🚀 Setting up Multilingual Translator Application"
echo "================================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing requirements..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# Flask Configuration
FLASK_ENV=development
PORT=5000

# Hugging Face Configuration (optional)
# HF_TOKEN=your_huggingface_token_here

# Application Configuration
MAX_TEXT_LENGTH=1000
CACHE_MODELS=true
LOG_LEVEL=INFO
EOF
    echo "✅ Created .env file"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To start the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the application: python3 run.py"
echo "3. Open your browser to: http://localhost:5000"
echo ""
echo "To run tests:"
echo "python3 test_app.py"
echo ""
echo "For deployment:"
echo "- Heroku: git push heroku main"
echo "- Docker: docker build -t translator . && docker run -p 5000:5000 translator"
