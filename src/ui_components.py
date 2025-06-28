import streamlit as st
import re

def apply_mcq_css():
    """Apply custom CSS for MCQ display"""
    st.markdown("""
    <style>
    /* MCQ Container Styling */
    .mcq-container {
        background: white;
        paddi    # If nquestions were parsed, show error message
    if total_questions == 0:
        st.error("⚠️ MCQ बनाउन सकिएन। कृपया फेरि प्रयास गर्नुहोस्।")
        return

    for i, block in enumerate(question_blocks, start=1):
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        border-left: 5px solid #667eea;
        animation: slideInRight 0.6s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Question Styling */
    .question-title {
        color: #2c3e50;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding: 1rem;
        background: rgba(102, 126, 234, 0.1);
        border-radius: 15px;
        border-left: 4px solid #667eea;
    }
    
    /* Option Styling */
    .stRadio > div {
        background: transparent;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .stRadio > div:hover {
        background: transparent;
        transform: none;
    }
    
    /* Button Styling for MCQ */
    .check-button > button {
        background: linear-gradient(45deg, #2ecc71, #27ae60);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.6rem 1.5rem;
        font-size: 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(46, 204, 113, 0.3);
        margin: 1rem 0;
    }
    
    .check-button > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(46, 204, 113, 0.4);
        background: linear-gradient(45deg, #27ae60, #2ecc71);
    }
    
    /* Success/Error Message Styling */
    .stAlert[data-baseweb="notification"] {
        border-radius: 15px;
        animation: bounceIn 0.6s ease-out;
        font-weight: 500;
    }
    
    @keyframes bounceIn {
        0% {
            opacity: 0;
            transform: scale(0.3);
        }
        50% {
            opacity: 1;
            transform: scale(1.05);
        }
        70% {
            transform: scale(0.9);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Divider Styling */
    .custom-divider {
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border: none;
        border-radius: 2px;
        margin: 2rem 0;
        animation: slideIn 0.8s ease-out;
    }
    
    @keyframes slideIn {
        from {
            width: 0;
        }
        to {
            width: 100%;
        }
    }
    
    /* Progress indicator */
    .progress-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
    }
    
    .progress-container h3 {
        color: #2c3e50 !important;
        margin: 0 !important;
        font-size: 1.3rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

def display_mcqs(mcq_text):
    apply_mcq_css()
    
    # Check if the mcq_text is actually an error message
    if mcq_text.startswith("❌ Error:"):
        st.error("API सेवामा समस्या भएको छ। कृपया API key जाँच गर्नुहोस् वा पछि प्रयास गर्नुहोस्।")
        with st.expander("Error Details"):
            st.text(mcq_text)
        return
    
    # Initialize session state for answers if not exists
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'show_results' not in st.session_state:
        st.session_state.show_results = {}
    if 'total_score' not in st.session_state:
        st.session_state.total_score = 0
    
    # Split by question number patterns (support both Nepali and Arabic numerals)
    # Try multiple patterns to parse questions
    question_blocks = []
    
    # Check if this is a fallback MCQ (contains the note)
    if "स्थानीय MCQ सिर्जना गरिएको छ" in mcq_text:
        # Remove the note for parsing
        mcq_text = mcq_text.split("स्थानीय MCQ सिर्जना गरिएको छ।")[1].strip()
    
    # Pattern 1: Try Nepali numerals (१. २. ३.)
    blocks = re.split(r'\n?\s*[१२३४५६७८९०]+\.\s*', mcq_text)
    if len([b for b in blocks if b.strip()]) > 1:
        question_blocks = [q.strip() for q in blocks if q.strip()]
    
    # Pattern 2: Try Arabic numerals (1. 2. 3.)
    if not question_blocks:
        blocks = re.split(r'\n?\s*\d+\.\s*', mcq_text)
        if len([b for b in blocks if b.strip()]) > 1:
            question_blocks = [q.strip() for q in blocks if q.strip()]
    
    # Pattern 3: Try splitting by question marks
    if not question_blocks:
        blocks = mcq_text.split('?')
        temp_blocks = []
        for i, block in enumerate(blocks[:-1]):  # Exclude last empty part
            # Add the question mark back and combine with options
            question_part = block + '?'
            if i + 1 < len(blocks):
                # Add the next part until we find another question or end
                next_part = blocks[i + 1]
                # Find where the next question starts
                lines = next_part.split('\n')
                option_lines = []
                for j, line in enumerate(lines):
                    if re.match(r'^\s*[१२३४५६७८९०\d]+\.\s*', line):
                        break
                    option_lines.append(line)
                question_part += '\n'.join(option_lines)
            temp_blocks.append(question_part.strip())
        if temp_blocks:
            question_blocks = temp_blocks
    
    # Pattern 4: If still no blocks, try splitting by "सही उत्तर:"
    if not question_blocks:
        parts = mcq_text.split('सही उत्तर:')
        if len(parts) > 1:
            question_blocks = []
            for i in range(len(parts) - 1):
                # Combine current part with its answer
                block = parts[i]
                if i > 0:  # Skip the first empty part
                    # Remove the previous answer from the beginning
                    lines = block.split('\n')
                    # Find where the new question starts
                    question_start = 0
                    for j, line in enumerate(lines):
                        if re.match(r'^\s*[१२३४५६७८९०\d]+\.\s*', line) or '?' in line:
                            question_start = j
                            break
                    block = '\n'.join(lines[question_start:])
                
                # Add the answer back
                if i + 1 < len(parts):
                    answer_line = parts[i + 1].split('\n')[0]
                    block += f'\nसही उत्तर: {answer_line}'
                    
                if block.strip():
                    question_blocks.append(block.strip())
    
    # Pattern 5: Last resort - treat the whole text as one question if it contains options
    if not question_blocks and ('क)' in mcq_text or 'क ' in mcq_text):
        question_blocks = [mcq_text.strip()]
    
    # Progress header
    total_questions = len(question_blocks)
    answered_questions = len([q for q in st.session_state.show_results.values() if q])
    
    # If no questions were parsed, show error message
    if total_questions == 0:
        st.error("⚠️ MCQ बनाउन सकिएन। कृपया फेरि प्रयास गर्नुहोस्।")
        return

    for i, block in enumerate(question_blocks, start=1):
        lines = block.split('\n')
        lines = [line.strip() for line in lines if line.strip()]  # Remove empty lines
        
        if len(lines) < 2:
            st.warning(f"⚠️ Question {i}: Not enough content to parse")
            continue

        # Find the question text (usually the first line or line with question mark)
        question_text = ""
        question_line_idx = 0
        
        for j, line in enumerate(lines):
            if '?' in line or '।' in line or not re.match(r'^[कखगघ]\)', line):
                question_text = line
                question_line_idx = j
                break
        
        if not question_text:
            question_text = lines[0]
            
        options = []
        
        # Extract options starting with Nepali letters (more flexible parsing)
        for line in lines[question_line_idx + 1:]:
            # Match both क) and क patterns
            match = re.match(r'^([कखगघ])\)?\s*(.+)', line.strip())
            if match:
                option_text = match.group(2).strip()
                if option_text and not option_text.startswith('सही उत्तर'):
                    options.append(option_text)
        
        # Skip if we don't have enough options
        if len(options) < 2:
            continue

        # MCQ Container
        st.markdown('<div class="mcq-container">', unsafe_allow_html=True)
        
        # Question Title
        st.markdown(f"""
        <div class="question-title">
            <strong>प्रश्न {i}: {question_text}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Store the selected answer in session state
        selected = st.radio(
            "उत्तर चयन गर्नुहोस्:", 
            options, 
            key=f"q{i}",
            index=0 if options else None  # Default to first option
        )
        if selected:
            st.session_state.user_answers[i] = selected

        # Check answer button
        st.markdown('<div class="check-button">', unsafe_allow_html=True)
        if st.button("✓ उत्तर जाँच गर्नुहोस्", key=f"btn{i}"):
            st.session_state.show_results[i] = True
        st.markdown('</div>', unsafe_allow_html=True)

        # Show result if button was clicked
        if st.session_state.show_results.get(i, False):
            correct_index = get_correct_index(question_text, block)
            if selected and correct_index is not None and selected in options and options.index(selected) == correct_index:
                st.success("🎉 उत्कृष्ट! तपाईंको उत्तर सही छ!")
                if i not in st.session_state.get('correct_answers', set()):
                    if 'correct_answers' not in st.session_state:
                        st.session_state.correct_answers = set()
                    st.session_state.correct_answers.add(i)
            else:
                if correct_index is not None and correct_index < len(options):
                    correct_answer = options[correct_index]
                else:
                    correct_answer = "उत्तर उपलब्ध छैन"
                st.error(f"❌ गलत उत्तर। सही उत्तर: **{correct_answer}**")
                
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Custom divider
        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    
    # Final score display
    if answered_questions == total_questions and total_questions > 0:
        correct_count = len(st.session_state.get('correct_answers', set()))
        score_percentage = (correct_count / total_questions) * 100
        
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea, #764ba2); 
                    color: white; border-radius: 20px; margin: 2rem 0; animation: fadeIn 1s ease-out;">
            <h2>🏆 अन्तिम नतिजा</h2>
            <h3>{}/{} सही उत्तरहरू</h3>
            <h1>{}%</h1>
            <p>{}</p>
        </div>
        """.format(
            correct_count, 
            total_questions, 
            int(score_percentage),
            get_performance_message(score_percentage)
        ), unsafe_allow_html=True)

def get_performance_message(score):
    """Get performance message based on score"""
    if score >= 90:
        return "🌟 उत्कृष्ट! तपाईं एक उत्कृष्ट विद्यार्थी हुनुहुन्छ!"
    elif score >= 75:
        return "👏 राम्रो! तपाईंको प्रदर्शन राम्रो छ!"
    elif score >= 50:
        return "👍 ठीक छ! अझै सुधार गर्न सकिन्छ!"
    else:
        return "📚 अझ अध्ययन गर्नुहोस्! तपाईं गर्न सक्नुहुन्छ!"


# Enhanced logic for correct answer that parses from MCQ text
def get_correct_index(question_text, mcq_block=""):
    """Return the correct answer index based on MCQ block parsing only."""
    
    # Try to extract from the MCQ block if it contains "सही उत्तर:"
    if "सही उत्तर:" in mcq_block:
        try:
            answer_line = mcq_block.split("सही उत्तर:")[1].strip().split('\n')[0].strip()
            # Map Nepali letters to indices
            letter_map = {'क': 0, 'ख': 1, 'ग': 2, 'घ': 3}
            if answer_line in letter_map:
                print(f"DEBUG: Found correct answer '{answer_line}' in MCQ block")
                return letter_map[answer_line]
        except Exception as e:
            print(f"DEBUG: Error parsing correct answer: {e}")
    
    # Default to first option if cannot parse the correct answer
    print(f"DEBUG: No explicit answer found, defaulting to index 0")
    return 0
