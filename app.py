import streamlit as st
from src.mcq_generator import generate_mcqs
from src.ui_components import display_mcqs

def load_stopwords():
    with open("data/nepali_stopwords.txt", "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def apply_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Remove default padding */
    .stApp > div:first-child > div:first-child > div:first-child {
        padding-top: 1rem;
    }
    
    /* Container styling */
    .content-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        margin: 1rem 0;
        animation: fadeInUp 0.8s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
        background: linear-gradient(45deg, #764ba2, #667eea);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Back button styling */
    .back-button > button {
        background: linear-gradient(45deg, #ff6b6b, #ffa726);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 1.5rem;
        font-size: 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.3);
    }
    
    .back-button > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        border-radius: 15px;
        border: 2px solid #e9ecef !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        font-family: 'Poppins', sans-serif !important;
        transition: all 0.3s ease;
        background: white !important;
        color: #2c3e50 !important;
        line-height: 1.6 !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.2) !important;
        background: white !important;
        color: #2c3e50 !important;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: #7f8c8d !important;
        opacity: 0.8 !important;
    }
    
    /* Text area label styling */
    .stTextArea > label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Text area container */
    .stTextArea {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Progress and caption styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
    }
    
    .stCaption {
        color: #7f8c8d !important;
        text-align: center;
        font-weight: 500;
    }
    
    /* Warning and success messages */
    .stAlert {
        border-radius: 15px;
        animation: slideInLeft 0.5s ease-out;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Spinner customization */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Smooth transitions for all elements */
    * {
        transition: all 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Nepali MCQ Generator", 
        layout="centered",
        page_icon="📝",
        initial_sidebar_state="collapsed"
    )
    
    apply_custom_css()
    
    # Custom title with animation
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; animation: slideInDown 1s ease-out;">
        <h1 style="color: white; font-size: 3rem; font-weight: 700; margin-bottom: 1rem; 
                   text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);">
             Nepali MCQ Generator
        </h1>
        <p style="color: rgba(255, 255, 255, 0.9); font-size: 1.2rem; margin-bottom: 2rem;">
            स्वचालित बहुविकल्पीय प्रश्न निर्माणकर्ता
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'mcq_generated' not in st.session_state:
        st.session_state.mcq_generated = False
    if 'mcq_text' not in st.session_state:
        st.session_state.mcq_text = ""
    
    stopwords = load_stopwords()
    
    # Check if MCQs are already generated
    if st.session_state.mcq_generated and st.session_state.mcq_text:
        # Show back button with custom styling
        st.markdown('<div class="back-button">', unsafe_allow_html=True)
        if st.button("← नयाँ पाठ राख्नुहोस्"):
            st.session_state.mcq_generated = False
            st.session_state.mcq_text = ""
            # Clear other session states
            if 'user_answers' in st.session_state:
                del st.session_state.user_answers
            if 'show_results' in st.session_state:
                del st.session_state.show_results
            if 'correct_answers' in st.session_state:
                del st.session_state.correct_answers
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display MCQs
        display_mcqs(st.session_state.mcq_text)
    else:
        # Show input form with enhanced styling in a white container
        st.markdown("""
        <div class="content-container">
            <div style="text-align: center; margin-bottom: 2rem;">
                <p style="font-size: 1.3rem; color: #34495e; line-height: 1.6; margin: 0;">
                    यहाँ तपाइँले नेपाली पाठ लेख्न सक्नुहुन्छ र बहुविकल्पीय प्रश्नहरू (MCQs) स्वतः निर्माण हुनेछ।
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced text area in a visible container
        st.markdown("""
        <div class="content-container">
            <h3 style="color: #2c3e50; margin-bottom: 1rem;">📝 पाठ सामग्री</h3>
        </div>
        """, unsafe_allow_html=True)
        
        text = st.text_area(
            "पाठ सामग्री यहाँ राख्नुहोस्:", 
            height=300,
            placeholder="यहाँ तपाईंको नेपाली पाठ टाइप गर्नुहोस् वा paste गर्नुहोस्...",
            help="कम्तिमा ५० अक्षरहरू आवश्यक छ"
        )
        
        # Progress indicator in a container
        if text:
            st.markdown('<div class="content-container">', unsafe_allow_html=True)
            char_count = len(text)
            if char_count < 50:
                st.progress(char_count / 50)
                st.caption(f"कम्तिमा ५० अक्षरहरू चाहिन्छ। हाल: {char_count} अक्षरहरू")
            else:
                st.success(f" तयार! {char_count} अक्षरहरू")
            st.markdown('</div>', unsafe_allow_html=True)

        if st.button(" MCQ बनाउनुहोस्"):
            if not text or len(text) < 50:
                st.warning(" कृपया ५० वा बढी अक्षरहरू भएको पाठ राख्नुहोस्।")
            else:
                with st.spinner(" MCQs बनाउँदै... कृपया पर्खनुहोस्।"):
                    mcq_text = generate_mcqs(text, stopwords, max_questions=5)
                    st.session_state.mcq_text = mcq_text
                    st.session_state.mcq_generated = True
                    st.rerun()


if __name__ == "__main__":
    main()
