import random

def analyze_text_content(text):
    """
    Simulates text moderation tracking.
    Matches keywords or passes details down to a processing function.
    """
    flagged_keywords = ['toxic', 'hate', 'spam', 'kill', 'attack']
    text_lower = text.lower()
    
    for word in flagged_keywords:
        if word in text_lower:
            return {
                "is_flagged": True,
                "flag_reason": f"Content triggered safety policies regarding: {word}",
                "confidence_score": round(random.uniform(0.85, 0.99), 2)
            }
            
    return {
        "is_flagged": False,
        "flag_reason": None,
        "confidence_score": round(random.uniform(0.0, 0.15), 2)
    }

def analyze_image_content(image_url):
    """
    Simulates computer vision processing on image assets.
    """
    if "nsfw" in image_url.lower() or "weapon" in image_url.lower():
        return {
            "is_flagged": True,
            "flag_reason": "Inappropriate visual material flagged.",
            "confidence_score": round(random.uniform(0.90, 0.98), 2)
        }
        
    return {
        "is_flagged": False,
        "flag_reason": None,
        "confidence_score": round(random.uniform(0.0, 0.10), 2)
    }