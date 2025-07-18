import json
import os
from flask import session

def load_translations(lang='en'):
    """Load translation file for specified language"""
    try:
        file_path = f"translations/{lang}.json"
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Fallback to English if language file doesn't exist
            with open("translations/en.json", 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading translations: {e}")
        return {}

def get_current_language():
    """Get current language from session or default to English"""
    return session.get('language', 'en')

def set_language(lang):
    """Set language in session"""
    if lang in ['en', 'ar']:
        session['language'] = lang
        return True
    return False

def get_text(key, lang=None):
    """Get translated text by key"""
    if lang is None:
        lang = get_current_language()
    
    translations = load_translations(lang)
    
    # Handle nested keys like 'nav.home'
    keys = key.split('.')
    text = translations
    
    for k in keys:
        if isinstance(text, dict) and k in text:
            text = text[k]
        else:
            return key  # Return key if translation not found
    
    return text

def get_localized_field(obj, field_name, lang=None):
    """Get localized field value from database object"""
    if lang is None:
        lang = get_current_language()
    
    field_key = f"{field_name}_{lang}"
    if hasattr(obj, field_key):
        return getattr(obj, field_key)
    else:
        # Fallback to English if localized field doesn't exist
        field_key = f"{field_name}_en"
        if hasattr(obj, field_key):
            return getattr(obj, field_key)
        else:
            return getattr(obj, field_name, '')