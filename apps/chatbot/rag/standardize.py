import re
import unicodedata

def clean_text_encoding(text):
    if not text:
        return ""
    
    try:
        text = text.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        
        text = ''.join(char for char in text if unicodedata.category(char)[0] != 'C' or char in '\n\t ')
        
        text = unicodedata.normalize('NFKC', text)
        
        return text
    except Exception as e:
        return ''.join(char for char in text if ord(char) < 128)

def preprocess_text(text):
    text = clean_text_encoding(text)
    text = text.lower()
    text = re.sub(r'\n+', '\n', text)
    return text