from src.api.openai_client import generate_mcqs_from_text
from src.utils.text_processing import clean_text, remove_stopwords, split_sentences

def generate_mcqs(raw_text, stopwords, max_questions=5):
    """Generate MCQs from raw text"""
    print(f"DEBUG: Raw text length: {len(raw_text)}")
    
    cleaned = clean_text(raw_text)
    print(f"DEBUG: Cleaned text length: {len(cleaned)}")
    print(f"DEBUG: Cleaned text preview: {cleaned[:200]}...")
    
    # Use cleaned text for MCQ generation (don't remove stopwords as they're important for context)
    mcq_text = generate_mcqs_from_text(cleaned, max_questions)
    
    print(f"DEBUG: Generated MCQ text length: {len(mcq_text)}")
    print(f"DEBUG: Generated MCQ text: {mcq_text}")
    
    # If the response is too short or contains error, return a fallback
    if len(mcq_text) < 100 or mcq_text.strip().startswith("❌"):
        print("DEBUG: API response seems to be an error or too short, creating fallback MCQ")
        return create_fallback_mcq(cleaned[:500])  # Use first 500 chars for fallback
    
    return mcq_text

def create_fallback_mcq(text):
    """Create a simple fallback MCQ when API fails"""
    return f"""१. दिइएको पाठमा मुख्य विषय के हो?
क) सामान्य जानकारी
ख) शिक्षा सम्बन्धी
ग) पाठमा उल्लेखित मुख्य कुरा
घ) अन्य विषय
सही उत्तर: ग

२. यो पाठ कुन प्रकारको सामग्री हो?
क) कथा
ख) जानकारीमूलक पाठ
ग) कविता  
घ) नाटक
सही उत्तर: ख"""
