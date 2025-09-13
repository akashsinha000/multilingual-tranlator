from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from transformers import MarianMTModel, MarianTokenizer
import torch
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Supported languages mapping
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh': 'Chinese',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'da': 'Danish',
    'no': 'Norwegian',
    'fi': 'Finnish',
    'pl': 'Polish',
    'tr': 'Turkish',
    'th': 'Thai',
    'vi': 'Vietnamese'
}

# Model cache to avoid reloading models
model_cache = {}

def get_model_name(source_lang, target_lang):
    """Get the Hugging Face model name for the language pair"""
    model_mapping = {
        ('en', 'es'): 'Helsinki-NLP/opus-mt-en-es',
        ('es', 'en'): 'Helsinki-NLP/opus-mt-es-en',
        ('en', 'fr'): 'Helsinki-NLP/opus-mt-en-fr',
        ('fr', 'en'): 'Helsinki-NLP/opus-mt-fr-en',
        ('en', 'de'): 'Helsinki-NLP/opus-mt-en-de',
        ('de', 'en'): 'Helsinki-NLP/opus-mt-de-en',
        ('en', 'it'): 'Helsinki-NLP/opus-mt-en-it',
        ('it', 'en'): 'Helsinki-NLP/opus-mt-it-en',
        ('en', 'pt'): 'Helsinki-NLP/opus-mt-en-pt',
        ('pt', 'en'): 'Helsinki-NLP/opus-mt-pt-en',
        ('en', 'ru'): 'Helsinki-NLP/opus-mt-en-ru',
        ('ru', 'en'): 'Helsinki-NLP/opus-mt-ru-en',
        ('en', 'ja'): 'Helsinki-NLP/opus-mt-en-jap',
        ('ja', 'en'): 'Helsinki-NLP/opus-mt-jap-en',
        ('en', 'ko'): 'Helsinki-NLP/opus-mt-en-ko',
        ('ko', 'en'): 'Helsinki-NLP/opus-mt-ko-en',
        ('en', 'zh'): 'Helsinki-NLP/opus-mt-en-zh',
        ('zh', 'en'): 'Helsinki-NLP/opus-mt-zh-en',
        ('en', 'ar'): 'Helsinki-NLP/opus-mt-en-ar',
        ('ar', 'en'): 'Helsinki-NLP/opus-mt-ar-en',
        ('en', 'hi'): 'Helsinki-NLP/opus-mt-en-hi',
        ('hi', 'en'): 'Helsinki-NLP/opus-mt-hi-en',
    }
    return model_mapping.get((source_lang, target_lang))

def load_translation_model(source_lang, target_lang):
    """Load or get cached translation model"""
    model_key = f"{source_lang}_{target_lang}"
    
    if model_key in model_cache:
        return model_cache[model_key]
    
    model_name = get_model_name(source_lang, target_lang)
    if not model_name:
        raise ValueError(f"Translation from {source_lang} to {target_lang} is not supported")
    
    try:
        logger.info(f"Loading model: {model_name}")
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        
        # Cache the model
        model_cache[model_key] = (tokenizer, model)
        return tokenizer, model
    except Exception as e:
        logger.error(f"Error loading model {model_name}: {str(e)}")
        raise

def translate_text(text, source_lang, target_lang):
    """Translate text from source language to target language"""
    try:
        tokenizer, model = load_translation_model(source_lang, target_lang)
        
        # Tokenize input
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        
        # Generate translation
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=512, num_beams=4, early_stopping=True)
        
        # Decode output
        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return translated_text
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@app.route('/manifest.json')
def manifest():
    """Serve the PWA manifest"""
    return app.send_static_file('manifest.json')

@app.route('/sw.js')
def service_worker():
    """Serve the service worker"""
    return app.send_static_file('sw.js')

@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Get list of supported languages"""
    return jsonify({
        'success': True,
        'languages': SUPPORTED_LANGUAGES
    })

@app.route('/api/translate', methods=['POST'])
def translate():
    """Translate text from one language to another"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        text = data.get('text', '').strip()
        source_lang = data.get('source_lang', '').lower()
        target_lang = data.get('target_lang', '').lower()
        
        # Validation
        if not text:
            return jsonify({
                'success': False,
                'error': 'Text is required'
            }), 400
        
        if not source_lang or not target_lang:
            return jsonify({
                'success': False,
                'error': 'Source and target languages are required'
            }), 400
        
        if source_lang not in SUPPORTED_LANGUAGES:
            return jsonify({
                'success': False,
                'error': f'Source language "{source_lang}" is not supported'
            }), 400
        
        if target_lang not in SUPPORTED_LANGUAGES:
            return jsonify({
                'success': False,
                'error': f'Target language "{target_lang}" is not supported'
            }), 400
        
        if source_lang == target_lang:
            return jsonify({
                'success': True,
                'translated_text': text,
                'source_lang': source_lang,
                'target_lang': target_lang
            })
        
        # Translate text
        translated_text = translate_text(text, source_lang, target_lang)
        
        return jsonify({
            'success': True,
            'translated_text': translated_text,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'original_text': text
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@app.route('/api/detect', methods=['POST'])
def detect_language():
    """Detect the language of the input text (simplified version)"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'Text is required'
            }), 400
        
        # Simple language detection based on character patterns
        # This is a basic implementation - in production, you'd use a proper language detection model
        detected_lang = 'en'  # Default to English
        
        # Check for specific character patterns
        if any('\u4e00' <= char <= '\u9fff' for char in text):  # Chinese characters
            detected_lang = 'zh'
        elif any('\u3040' <= char <= '\u309f' or '\u30a0' <= char <= '\u30ff' for char in text):  # Japanese
            detected_lang = 'ja'
        elif any('\uac00' <= char <= '\ud7af' for char in text):  # Korean
            detected_lang = 'ko'
        elif any('\u0600' <= char <= '\u06ff' for char in text):  # Arabic
            detected_lang = 'ar'
        elif any('\u0900' <= char <= '\u097f' for char in text):  # Hindi
            detected_lang = 'hi'
        elif any('\u0400' <= char <= '\u04ff' for char in text):  # Cyrillic (Russian)
            detected_lang = 'ru'
        
        return jsonify({
            'success': True,
            'detected_language': detected_lang,
            'language_name': SUPPORTED_LANGUAGES.get(detected_lang, 'Unknown')
        })
        
    except Exception as e:
        logger.error(f"Language detection error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Language detection failed'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Multilingual Translator API',
        'supported_languages': len(SUPPORTED_LANGUAGES)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Multilingual Translator API on port {port}")
    logger.info(f"Supported languages: {list(SUPPORTED_LANGUAGES.keys())}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
