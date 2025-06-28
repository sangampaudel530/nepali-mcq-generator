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
    
    return mcq_text
