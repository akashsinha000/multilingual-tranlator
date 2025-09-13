# Multilingual Language Translator

A real-time multilingual translation application built with Python Flask backend and Hugging Face models, featuring a mobile-friendly web interface.

## Features

- **Real-time Translation**: Fast and accurate translations powered by Hugging Face models
- **20+ Languages**: Support for major world languages including English, Spanish, French, German, Japanese, Korean, Chinese, Arabic, Hindi, and more
- **Mobile-Friendly**: Responsive design optimized for mobile devices and tablets
- **Auto Language Detection**: Automatic language detection for unknown text
- **Text-to-Speech**: Speak translations aloud
- **Copy to Clipboard**: Easy text copying functionality
- **PWA Support**: Progressive Web App capabilities for offline usage
- **REST API**: Clean API endpoints for integration with other applications

## Supported Languages

- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Japanese (ja)
- Korean (ko)
- Chinese (zh)
- Arabic (ar)
- Hindi (hi)
- Dutch (nl)
- Swedish (sv)
- Danish (da)
- Norwegian (no)
- Finnish (fi)
- Polish (pl)
- Turkish (tr)
- Thai (th)
- Vietnamese (vi)

## Technology Stack

- **Backend**: Python, Flask
- **AI Models**: Hugging Face Transformers (MarianMT)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with responsive design
- **Deployment**: Gunicorn, Heroku-ready

## Installation

### Prerequisites

- Python 3.9+
- pip
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd multilingual-translator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and go to `http://localhost:5000`

## API Endpoints

### Get Supported Languages
```
GET /api/languages
```

**Response:**
```json
{
    "success": true,
    "languages": {
        "en": "English",
        "es": "Spanish",
        ...
    }
}
```

### Translate Text
```
POST /api/translate
```

**Request Body:**
```json
{
    "text": "Hello, world!",
    "source_lang": "en",
    "target_lang": "es"
}
```

**Response:**
```json
{
    "success": true,
    "translated_text": "¡Hola, mundo!",
    "source_lang": "en",
    "target_lang": "es",
    "original_text": "Hello, world!"
}
```

### Detect Language
```
POST /api/detect
```

**Request Body:**
```json
{
    "text": "Bonjour le monde"
}
```

**Response:**
```json
{
    "success": true,
    "detected_language": "fr",
    "language_name": "French"
}
```

### Health Check
```
GET /health
```

**Response:**
```json
{
    "status": "healthy",
    "service": "Multilingual Translator API",
    "supported_languages": 21
}
```

## Usage

### Web Interface

1. **Select Languages**: Choose source and target languages from the dropdown menus
2. **Enter Text**: Type or paste text in the source language
3. **Translate**: Click the "Translate" button or use Ctrl+Enter
4. **Copy/Speak**: Use the action buttons to copy text or hear pronunciation
5. **Swap Languages**: Click the swap button to reverse the translation direction

### Mobile Features

- **Touch-friendly**: Large buttons and touch targets
- **Responsive Design**: Adapts to different screen sizes
- **Offline Support**: Basic functionality works offline
- **PWA Installation**: Can be installed as a mobile app

## Configuration

### Environment Variables

- `FLASK_ENV`: Environment (development/production)
- `PORT`: Server port (default: 5000)
- `MAX_TEXT_LENGTH`: Maximum text length for translation (default: 1000)
- `CACHE_MODELS`: Whether to cache models (default: true)
- `LOG_LEVEL`: Logging level (default: INFO)
- `HF_TOKEN`: Hugging Face API token (optional)

### Model Configuration

The application uses Helsinki-NLP MarianMT models for translation. Models are automatically downloaded and cached on first use.

## Deployment

### Heroku Deployment

1. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

2. **Set environment variables**
   ```bash
   heroku config:set FLASK_ENV=production
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

### Docker Deployment

1. **Build image**
   ```bash
   docker build -t multilingual-translator .
   ```

2. **Run container**
   ```bash
   docker run -p 5000:5000 multilingual-translator
   ```

## Performance Optimization

- **Model Caching**: Models are cached in memory to avoid reloading
- **Text Length Limits**: Configurable maximum text length
- **Error Handling**: Comprehensive error handling and user feedback
- **Responsive Design**: Optimized for mobile and desktop

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Hugging Face](https://huggingface.co/) for providing the translation models
- [Helsinki-NLP](https://huggingface.co/Helsinki-NLP) for the MarianMT models
- [Flask](https://flask.palletsprojects.com/) for the web framework

## Support

For support, email support@example.com or create an issue in the repository.
