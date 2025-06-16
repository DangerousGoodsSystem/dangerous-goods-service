import re
import unicodedata

def clean_text_encoding(text):
    """Làm sạch các ký tự encoding lỗi"""
    if not text:
        return ""
    
    try:
        # Loại bỏ các surrogate characters
        text = text.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        
        # Loại bỏ các ký tự control characters
        text = ''.join(char for char in text if unicodedata.category(char)[0] != 'C' or char in '\n\t ')
        
        # Chuẩn hóa Unicode
        text = unicodedata.normalize('NFKC', text)
        
        return text
    except Exception as e:
        print(f"⚠️ Lỗi khi làm sạch text: {e}")
        # Fallback: chỉ giữ các ký tự ASCII an toàn
        return ''.join(char for char in text if ord(char) < 128)

def preprocess_text(text):
    """Chuẩn hóa về chữ thường và newline"""
    text = clean_text_encoding(text)
    text = text.lower()  # Chuyển về chữ thường
    text = re.sub(r'\n+', '\n', text)  # Nhiều \n thành 1 \n
    return text