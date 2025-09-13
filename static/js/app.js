class TranslatorApp {
    constructor() {
        this.languages = {};
        this.isTranslating = false;
        this.autoTranslateTimeout = null;
        this.autoTranslateEnabled = false;
        this.init();
    }

    async init() {
        await this.loadLanguages();
        this.setupEventListeners();
        this.updateCharacterCount();
    }

    async loadLanguages() {
        try {
            const response = await fetch('/api/languages');
            const data = await response.json();
            
            if (data.success) {
                this.languages = data.languages;
                this.populateLanguageSelectors();
            } else {
                this.showToast('Failed to load languages', 'error');
            }
        } catch (error) {
            console.error('Error loading languages:', error);
            this.showToast('Failed to load languages', 'error');
        }
    }

    populateLanguageSelectors() {
        const sourceSelect = document.getElementById('source-lang');
        const targetSelect = document.getElementById('target-lang');

        // Clear existing options
        sourceSelect.innerHTML = '<option value="">Select language...</option>';
        targetSelect.innerHTML = '<option value="">Select language...</option>';

        // Add language options
        Object.entries(this.languages).forEach(([code, name]) => {
            const sourceOption = new Option(name, code);
            const targetOption = new Option(name, code);
            
            sourceSelect.add(sourceOption);
            targetSelect.add(targetOption);
        });

        // Set default values
        sourceSelect.value = 'en';
        targetSelect.value = 'es';
    }

    setupEventListeners() {
        // Translate button
        document.getElementById('translate-btn').addEventListener('click', () => {
            this.translate();
        });

        // Swap languages button
        document.getElementById('swap-languages').addEventListener('click', () => {
            this.swapLanguages();
        });

        // Clear text button
        document.getElementById('clear-text').addEventListener('click', () => {
            this.clearText();
        });

        // Copy buttons
        document.getElementById('copy-source').addEventListener('click', () => {
            this.copyText('source-text');
        });

        document.getElementById('copy-translation').addEventListener('click', () => {
            this.copyText('translated-text');
        });

        // Detect language button
        document.getElementById('detect-lang').addEventListener('click', () => {
            this.detectLanguage();
        });

        // Speak translation button
        document.getElementById('speak-translation').addEventListener('click', () => {
            this.speakTranslation();
        });

        // Character count update and auto-translate
        document.getElementById('source-text').addEventListener('input', () => {
            this.updateCharacterCount();
            this.handleAutoTranslate();
        });

        // Enter key to translate
        document.getElementById('source-text').addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.translate();
            }
        });

        // Auto-translate on language change
        document.getElementById('source-lang').addEventListener('change', () => {
            this.updateTranslationInfo();
            this.handleAutoTranslate();
        });

        document.getElementById('target-lang').addEventListener('change', () => {
            this.updateTranslationInfo();
            this.handleAutoTranslate();
        });

        // Add auto-translate toggle button
        this.addAutoTranslateToggle();
    }

    async translate() {
        const sourceText = document.getElementById('source-text').value.trim();
        const sourceLang = document.getElementById('source-lang').value;
        const targetLang = document.getElementById('target-lang').value;

        if (!sourceText) {
            this.showToast('Please enter text to translate', 'error');
            return;
        }

        if (!sourceLang || !targetLang) {
            this.showToast('Please select source and target languages', 'error');
            return;
        }

        if (sourceLang === targetLang) {
            document.getElementById('translated-text').value = sourceText;
            this.updateTranslationInfo();
            return;
        }

        this.showLoading(true);

        try {
            const response = await fetch('/api/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: sourceText,
                    source_lang: sourceLang,
                    target_lang: targetLang
                })
            });

            const data = await response.json();

            if (data.success) {
                document.getElementById('translated-text').value = data.translated_text;
                this.updateTranslationInfo();
                this.showToast('Translation completed successfully!', 'success');
            } else {
                this.showToast(data.error || 'Translation failed', 'error');
            }
        } catch (error) {
            console.error('Translation error:', error);
            this.showToast('Network error. Please try again.', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async detectLanguage() {
        const sourceText = document.getElementById('source-text').value.trim();

        if (!sourceText) {
            this.showToast('Please enter text to detect language', 'error');
            return;
        }

        try {
            const response = await fetch('/api/detect', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: sourceText
                })
            });

            const data = await response.json();

            if (data.success) {
                document.getElementById('source-lang').value = data.detected_language;
                this.updateTranslationInfo();
                this.showToast(`Detected language: ${data.language_name}`, 'info');
            } else {
                this.showToast(data.error || 'Language detection failed', 'error');
            }
        } catch (error) {
            console.error('Language detection error:', error);
            this.showToast('Language detection failed', 'error');
        }
    }

    swapLanguages() {
        const sourceLang = document.getElementById('source-lang').value;
        const targetLang = document.getElementById('target-lang').value;
        const sourceText = document.getElementById('source-text').value;
        const translatedText = document.getElementById('translated-text').value;

        // Swap language selections
        document.getElementById('source-lang').value = targetLang;
        document.getElementById('target-lang').value = sourceLang;

        // Swap text content
        document.getElementById('source-text').value = translatedText;
        document.getElementById('translated-text').value = sourceText;

        this.updateTranslationInfo();
        this.updateCharacterCount();
        this.showToast('Languages swapped!', 'info');
    }

    clearText() {
        document.getElementById('source-text').value = '';
        document.getElementById('translated-text').value = '';
        this.updateCharacterCount();
        this.showToast('Text cleared', 'info');
    }

    async copyText(elementId) {
        const text = document.getElementById(elementId).value;
        
        if (!text) {
            this.showToast('No text to copy', 'error');
            return;
        }

        try {
            await navigator.clipboard.writeText(text);
            this.showToast('Text copied to clipboard!', 'success');
        } catch (error) {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            this.showToast('Text copied to clipboard!', 'success');
        }
    }

    speakTranslation() {
        const text = document.getElementById('translated-text').value;
        const targetLang = document.getElementById('target-lang').value;

        if (!text) {
            this.showToast('No translation to speak', 'error');
            return;
        }

        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            
            // Set language based on target language
            const langMap = {
                'en': 'en-US',
                'es': 'es-ES',
                'fr': 'fr-FR',
                'de': 'de-DE',
                'it': 'it-IT',
                'pt': 'pt-PT',
                'ru': 'ru-RU',
                'ja': 'ja-JP',
                'ko': 'ko-KR',
                'zh': 'zh-CN',
                'ar': 'ar-SA',
                'hi': 'hi-IN'
            };

            utterance.lang = langMap[targetLang] || 'en-US';
            utterance.rate = 0.9;
            utterance.pitch = 1;
            utterance.volume = 0.8;

            speechSynthesis.speak(utterance);
            this.showToast('Speaking translation...', 'info');
        } else {
            this.showToast('Speech synthesis not supported', 'error');
        }
    }

    updateCharacterCount() {
        const text = document.getElementById('source-text').value;
        const charCount = text.length;
        document.getElementById('char-count').textContent = charCount;
    }

    updateTranslationInfo() {
        const sourceLang = document.getElementById('source-lang').value;
        const targetLang = document.getElementById('target-lang').value;
        const sourceText = document.getElementById('source-text').value;

        if (sourceLang && targetLang) {
            document.getElementById('source-lang-name').textContent = this.languages[sourceLang] || sourceLang;
            document.getElementById('target-lang-name').textContent = this.languages[targetLang] || targetLang;
            document.getElementById('translation-info').style.display = 'flex';
        } else {
            document.getElementById('translation-info').style.display = 'none';
        }
    }

    showLoading(show) {
        const overlay = document.getElementById('loading-overlay');
        overlay.style.display = show ? 'flex' : 'none';
    }

    showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.className = `toast ${type}`;
        toast.classList.add('show');

        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    addAutoTranslateToggle() {
        const translateButtonContainer = document.querySelector('.translate-button-container');
        const autoTranslateToggle = document.createElement('button');
        autoTranslateToggle.id = 'auto-translate-toggle';
        autoTranslateToggle.className = 'auto-translate-btn';
        autoTranslateToggle.innerHTML = '<i class="fas fa-magic"></i> Auto Translate';
        autoTranslateToggle.title = 'Toggle automatic translation';
        
        autoTranslateToggle.addEventListener('click', () => {
            this.toggleAutoTranslate();
        });

        translateButtonContainer.appendChild(autoTranslateToggle);
    }

    toggleAutoTranslate() {
        this.autoTranslateEnabled = !this.autoTranslateEnabled;
        const toggle = document.getElementById('auto-translate-toggle');
        
        if (this.autoTranslateEnabled) {
            toggle.classList.add('active');
            toggle.innerHTML = '<i class="fas fa-magic"></i> Auto Translate ON';
            this.showToast('Auto-translate enabled', 'success');
        } else {
            toggle.classList.remove('active');
            toggle.innerHTML = '<i class="fas fa-magic"></i> Auto Translate';
            this.showToast('Auto-translate disabled', 'info');
        }
    }

    handleAutoTranslate() {
        if (!this.autoTranslateEnabled) return;

        const sourceText = document.getElementById('source-text').value.trim();
        const sourceLang = document.getElementById('source-lang').value;
        const targetLang = document.getElementById('target-lang').value;

        // Clear existing timeout
        if (this.autoTranslateTimeout) {
            clearTimeout(this.autoTranslateTimeout);
        }

        // Only auto-translate if we have text and both languages selected
        if (sourceText && sourceLang && targetLang && sourceLang !== targetLang) {
            // Debounce the translation to avoid too many API calls
            this.autoTranslateTimeout = setTimeout(() => {
                this.translate();
            }, 1000); // Wait 1 second after user stops typing
        }
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TranslatorApp();
});

// Service Worker registration for PWA capabilities
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Handle online/offline status
window.addEventListener('online', () => {
    const toast = document.getElementById('toast');
    toast.textContent = 'Connection restored!';
    toast.className = 'toast success';
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2000);
});

window.addEventListener('offline', () => {
    const toast = document.getElementById('toast');
    toast.textContent = 'You are offline. Some features may not work.';
    toast.className = 'toast error';
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3000);
});
