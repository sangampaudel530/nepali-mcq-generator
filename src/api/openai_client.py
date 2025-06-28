import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from secrets in Streamlit
import streamlit as st
api_key = st.secrets["GEMINI_API_KEY"]

#for local 
# load_dotenv()  # Uncomment if using local .env file
# api_key = os.getenv("GEMINI_API_KEY")  # Uncomment if using local


# Configure Gemini AI
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
else:
    print("WARNING: No Gemini API key found in .env file")
    model = None

def generate_mcqs_from_text(text, max_questions=5):
    """Generate MCQs using Gemini 2.5 based on input text content"""
    
    if not model:
        return "❌ Error: Gemini API key not configured. Please add GEMINI_API_KEY to your .env file."
    
    prompt = f"""
तपाईं एक शिक्षाविद् हुनुहुन्छ जसको काम शिक्षात्मक उद्देश्यका लागि तथ्यमा आधारित बहुविकल्पीय प्रश्नहरू (MCQs) तयार गर्नु हो।

कृपया तलको अनुच्छेदको आधारमा {max_questions} वटा MCQs नेपाली भाषामा तयार गर्नुहोस्। निम्न निर्देशनहरू पालना गर्नुहोस्:

🔹 अनुच्छेदमा उल्लेखित तथ्यहरूमा आधारित प्रश्नहरू मात्र बनाउनुहोस्।
🔹 हरेक प्रश्नमा चार विकल्पहरू (क, ख, ग, घ) राख्नुहोस्।
🔹 एक मात्र सही उत्तर हुनु पर्नेछ।
🔹 विकल्पहरू यथासम्भव अर्थपूर्ण र भ्रामक नहुने बनाउनुहोस्।
🔹 कुनै पनि अतिरिक्त व्याख्या नगर्नुहोस्।
🔹 सही उत्तर स्पष्ट रूपमा उल्लेख गर्नुहोस्: "सही उत्तर: ख" जस्तै।
🔹 अनुच्छेदमा नभएका कुराहरूको बारेमा प्रश्न नगर्नुहोस्।

अनुच्छेद:
{text}

आउटपुटको ढाँचा:
१. प्रश्न?
क) विकल्प A
ख) विकल्प B
ग) विकल्प C
घ) विकल्प D
सही उत्तर: ख

२. प्रश्न?
क) विकल्प A
ख) विकल्प B
ग) विकल्प C
घ) विकल्प D
सही उत्तर: ग

केवल MCQs फिर्ता गर्नुहोस्, अन्य कुनै पाठ नदिनुहोस्।
"""

    try:
        print(f"DEBUG: Generating MCQs using Gemini for text: {text[:100]}...")
        
        response = model.generate_content(prompt)
        result = response.text.strip()
        
        print("DEBUG: Successfully generated MCQ content from Gemini:")
        print(result[:200] + "..." if len(result) > 200 else result)
        print("=" * 50)
        
        return result
        
    except Exception as e:
        error_msg = f"❌ Error generating MCQs: {str(e)}"
        print(f"DEBUG: Gemini API Error: {error_msg}")
        return error_msg


