from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
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

# Mock translation dictionary for demonstration
MOCK_TRANSLATIONS = {
    ('en', 'es'): {
        'hello': 'hola',
        'world': 'mundo',
        'good morning': 'buenos días',
        'thank you': 'gracias',
        'how are you': '¿cómo estás?',
        'goodbye': 'adiós'
    },
    ('es', 'en'): {
        'hola': 'hello',
        'mundo': 'world',
        'buenos días': 'good morning',
        'gracias': 'thank you',
        '¿cómo estás?': 'how are you',
        'adiós': 'goodbye'
    },
    ('en', 'fr'): {
        'hello': 'bonjour',
        'world': 'monde',
        'good morning': 'bonjour',
        'thank you': 'merci',
        'how are you': 'comment allez-vous',
        'goodbye': 'au revoir'
    },
    ('fr', 'en'): {
        'bonjour': 'hello',
        'monde': 'world',
        'merci': 'thank you',
        'comment allez-vous': 'how are you',
        'au revoir': 'goodbye'
    },
    ('en', 'de'): {
        'hello': 'hallo',
        'world': 'welt',
        'good morning': 'guten morgen',
        'thank you': 'danke',
        'how are you': 'wie geht es dir',
        'goodbye': 'auf wiedersehen'
    },
    ('de', 'en'): {
        'hallo': 'hello',
        'welt': 'world',
        'guten morgen': 'good morning',
        'danke': 'thank you',
        'wie geht es dir': 'how are you',
        'auf wiedersehen': 'goodbye'
    }
}

def mock_translate_text(text, source_lang, target_lang):
    """Mock translation function for demonstration"""
    text_lower = text.lower().strip()
    
    # Check if we have a direct translation
    if (source_lang, target_lang) in MOCK_TRANSLATIONS:
        translations = MOCK_TRANSLATIONS[(source_lang, target_lang)]
        if text_lower in translations:
            return translations[text_lower]
    
    # If no direct translation, return a mock response
    mock_responses = {
        'es': f"[Traducido al español] {text}",
        'fr': f"[Traduit en français] {text}",
        'de': f"[Ins Deutsche übersetzt] {text}",
        'it': f"[Tradotto in italiano] {text}",
        'pt': f"[Traduzido para português] {text}",
        'ru': f"[Переведено на русский] {text}",
        'ja': f"[日本語に翻訳] {text}",
        'ko': f"[한국어로 번역] {text}",
        'zh': f"[翻译成中文] {text}",
        'ar': f"[مترجم إلى العربية] {text}",
        'hi': f"[हिंदी में अनुवादित] {text}",
        'nl': f"[Vertaald naar het Nederlands] {text}",
        'sv': f"[Översatt till svenska] {text}",
        'da': f"[Oversat til dansk] {text}",
        'no': f"[Oversatt til norsk] {text}",
        'fi': f"[Käännetty suomeksi] {text}",
        'pl': f"[Przetłumaczone na polski] {text}",
        'tr': f"[Türkçeye çevrildi] {text}",
        'th': f"[แปลเป็นภาษาไทย] {text}",
        'vi': f"[Được dịch sang tiếng Việt] {text}"
    }
    
    return mock_responses.get(target_lang, f"[Translated to {target_lang}] {text}")

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
        
        # Translate text using mock function
        translated_text = mock_translate_text(text, source_lang, target_lang)
        
        return jsonify({
            'success': True,
            'translated_text': translated_text,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'original_text': text
        })
        
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
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
        elif any(char in 'ñáéíóúü' for char in text.lower()):  # Spanish
            detected_lang = 'es'
        elif any(char in 'àâäéèêëïîôöùûüÿç' for char in text.lower()):  # French
            detected_lang = 'fr'
        elif any(char in 'äöüß' for char in text.lower()):  # German
            detected_lang = 'de'
        
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
        'service': 'Multilingual Translator API (Demo Version)',
        'supported_languages': len(SUPPORTED_LANGUAGES),
        'note': 'This is a demo version with mock translations. For production use, install transformers and torch.'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Multilingual Translator API (Demo) on port {port}")
    logger.info(f"Supported languages: {list(SUPPORTED_LANGUAGES.keys())}")
    logger.info("Note: This is a demo version with mock translations")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
