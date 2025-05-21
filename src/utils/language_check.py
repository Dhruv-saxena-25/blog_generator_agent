from langdetect import detect


# Helper function to detect English language
def is_english(text):    
    ## Ensure we have enough text to analyse
    
    if not text or len(text.strip()) < 50:
        return False
    
    try:
        return detect(text) == "en"
    
    except:
        # If detection fails, use a more robust approach
        common_english_words = ['the', 'and', 'in', 'to', 'of', 'is', 'for', 'with', 'on', 'that', 
                              'this', 'are', 'was', 'be', 'have', 'it', 'not', 'they', 'by', 'from']
        
        text_lower = text.lower()
        # Count occurrences of common English words
        english_word_count = sum(1 for word in common_english_words if f" {word} " in f" {text_lower}")
        # Calculate ratio of English words to text length
        text_words = len(text_lower.split())
        if text_words == 0:  # Avoid division by zero
            return False        
        english_ratio = english_word_count / min(20, text_words)  # Cap at 20 to avoid skew
        return english_word_count >= 5 or english_ratio > 0.25  # More stringent criteria



         
    