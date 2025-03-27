

import streamlit as st
import requests
import random
import re
import nltk
from nltk.tokenize import sent_tokenize
import time
import json
import logging

logging.basicConfig(level=logging.INFO)

# Download necessary NLTK data
try:
    nltk.download('punkt_tab')
except:
    st.warning("NLTK punkt download failed. Some features may not work correctly.")

# Set up the Streamlit app
st.set_page_config(page_title="AI Text Humanizer", page_icon="🤖→🧠", layout="wide")

# Base URL for Ollama API
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Function to communicate with Ollama using only the phi3 model
def query_ollama(prompt, temperature=0.8, max_tokens=2000):
    model = "phi3"
    logging.info(f"Querying Ollama with model: {model}")
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        logging.info(f"Sending request to: {OLLAMA_API_URL}")
        response = requests.post(OLLAMA_API_URL, json=data)
        logging.info(f"Response status code: {response.status_code}")
        response.raise_for_status()
        
        # Handle the response from Ollama
        full_response = ""
        
        # Check if response is JSON
        try:
            json_response = response.json()
            if "response" in json_response:
                return json_response["response"]
        except:
            # Try to parse as streaming response
            for line in response.text.strip().split('\n'):
                if line:
                    try:
                        json_response = json.loads(line)
                        if "response" in json_response:
                            full_response += json_response["response"]
                    except:
                        pass
            return full_response
            
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with Ollama: {e}")
        if hasattr(e, 'response') and e.response:
            st.error(f"Response status: {e.response.status_code}")
            st.error(f"Response text: {e.response.text}")
        return None

# Function to humanize text using phi3 with an enhanced prompt
def humanize_text(text, temperature):
    # Enhanced prompt for more natural, human-like text
    prompt = f"""
    Please rewrite the following text so that it sounds as if it were written naturally by a human. 
    Transform the text to have an "Extreme" level of humanization. Follow these instructions closely:
    
    - Maintain the original meaning and information.
    - Use varied sentence structures and lengths.
    - Incorporate occasional filler words and conversational transitions.
    - Use a mix of formal and informal language including contractions.
    - Introduce slight redundancies and minor imperfections to emulate natural thought processes.
    - Allow for tangential observations or asides that do not detract from the main message.
    - Avoid overly structured or clinical formatting.
    - Infuse personality and warmth in the wording.
    
    Here is the text to be rewritten:
    
    {text}
    
    Ensure the final output reads as a perfect blend of clear information and genuine human expression.
    """
    
    # Query Ollama with the enhanced prompt
    humanized_text = query_ollama(prompt, temperature=temperature)
    return humanized_text

# Function to implement additional humanization techniques
def additional_humanization(text, techniques):
    if not text:
        return text
        
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    if "typos" in techniques and random.random() < 0.4:
        common_typos = {
            "the": ["teh", "hte"],
            "and": ["adn", "nad"],
            "that": ["taht", "tht"],
            "with": ["wtih", "wiht"],
            "this": ["tihs", "thsi"],
            "from": ["form", "fro"],
            "have": ["ahve", "hvae"],
            "would": ["woudl", "wuold"],
            "could": ["cuold", "coudl"],
            "their": ["thier", "theri"],
            "there": ["tehre", "ther"],
            "your": ["yoru", "yuor"],
            "because": ["becuase", "becasue"]
        }
        for i in range(len(sentences)):
            if random.random() < 0.2:
                words = sentences[i].split()
                for j in range(len(words)):
                    if words[j].lower() in common_typos and random.random() < 0.3:
                        if words[j][0].isupper():
                            words[j] = random.choice(common_typos[words[j].lower()]).capitalize()
                        else:
                            words[j] = random.choice(common_typos[words[j].lower()])
                sentences[i] = ' '.join(words)
    
    if "punctuation" in techniques:
        for i in range(len(sentences)):
            if random.random() < 0.15:
                if sentences[i].endswith('.'):
                    sentences[i] = sentences[i][:-1] + '..'
                elif sentences[i].endswith('!'):
                    sentences[i] = sentences[i][:-1] + '!!'
                elif sentences[i].endswith('?'):
                    sentences[i] = sentences[i][:-1] + '??'
                if len(sentences[i]) > 30 and random.random() < 0.5:
                    words = sentences[i].split()
                    if len(words) > 6:
                        splice_point = random.randint(3, len(words) - 3)
                        if not words[splice_point-1].endswith(',') and not words[splice_point-1].endswith(';'):
                            words[splice_point-1] = words[splice_point-1] + (',' if random.random() < 0.7 else ';')
                        sentences[i] = ' '.join(words)
    
    if "repetition" in techniques:
        for i in range(len(sentences)):
            if random.random() < 0.1:
                words = sentences[i].split()
                if len(words) > 4:
                    repeat_index = random.randint(0, len(words) - 1)
                    if len(words[repeat_index]) > 3 and not words[repeat_index].endswith((',', '.')):
                        words.insert(repeat_index + 1, words[repeat_index])
                        sentences[i] = ' '.join(words)
    
    if "formatting" in techniques:
        for i in range(len(sentences)):
            if random.random() < 0.05:
                words = sentences[i].split()
                if len(words) > 3:
                    emphasis_index = random.randint(0, len(words) - 1)
                    if len(words[emphasis_index]) > 3 and not re.search(r'[.,:;!?]', words[emphasis_index]):
                        words[emphasis_index] = words[emphasis_index].upper()
                        sentences[i] = ' '.join(words)
            if random.random() < 0.08:
                words = sentences[i].split()
                if len(words) > 3:
                    emphasis_index = random.randint(0, len(words) - 1)
                    if len(words[emphasis_index]) > 3 and not re.search(r'[.,:;!?]', words[emphasis_index]):
                        words[emphasis_index] = f"*{words[emphasis_index]}*" if random.random() < 0.5 else f"**{words[emphasis_index]}**"
                        sentences[i] = ' '.join(words)
    
    return ' '.join(sentences)

# Main app layout
st.title("🤖→🧠 AI Text Humanizer")
st.markdown("""
This app transforms AI-generated text into highly natural, human-like writing by leveraging advanced humanization techniques.
""")

# Sidebar configuration for advanced options (model is now fixed to phi3 and humanization level is Extreme)
st.sidebar.title("Advanced Settings")
st.sidebar.markdown("**Model:** phi3 (fixed)")
st.sidebar.markdown("**Humanization Level:** Extreme (fixed)")

# Temperature setting remains adjustable
temperature = st.sidebar.slider("Temperature", min_value=0.1, max_value=1.0, value=0.8, step=0.1)

# Additional techniques settings
st.sidebar.subheader("Additional Techniques")
add_typos = st.sidebar.checkbox("Add occasional typos", value=False)
vary_punctuation = st.sidebar.checkbox("Vary punctuation", value=True)
add_repetition = st.sidebar.checkbox("Add natural repetition", value=False)
adjust_formatting = st.sidebar.checkbox("Adjust formatting", value=True)

# Create tabs
tab1, tab2, tab3 = st.tabs(["Text Humanizer", "AI Detection Check", "About"])

with tab1:
    input_text = st.text_area("Enter AI-generated text to humanize:", height=200)
    
    if st.button("Humanize Text"):
        if not input_text:
            st.warning("Please enter some text to humanize.")
        else:
            with st.spinner("Processing with Ollama..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                # Use enhanced humanization (with phi3 and Extreme level)
                humanized_text = humanize_text(input_text, temperature=temperature)
                
                techniques = []
                if add_typos:
                    techniques.append("typos")
                if vary_punctuation:
                    techniques.append("punctuation")
                if add_repetition:
                    techniques.append("repetition")
                if adjust_formatting:
                    techniques.append("formatting")
                
                if techniques:
                    humanized_text = additional_humanization(humanized_text, techniques)
                    
                if humanized_text is not None:
                    st.subheader("Humanized Text:")
                    st.write(humanized_text)
                    st.text_area("Copy this text:", value=humanized_text, height=200)
                    
                    st.subheader("Text Statistics")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Original Word Count", len(input_text.split()))
                        st.metric("Original Character Count", len(input_text))
                    
                    with col2:
                        st.metric("Humanized Word Count", len(humanized_text.split()))
                        st.metric("Humanized Character Count", len(humanized_text))
                else:
                    st.error("Failed to generate humanized text. Please check Ollama setup and try again.") 

with tab2:
    st.markdown("""
    ## AI Detection Check
    
    This feature simulates how your text might perform against AI detection tools.
    
    **Note:** This is a heuristic estimation based on common detection patterns.
    """)
    
    check_text = st.text_area("Paste text to check:", height=200)
    
    if st.button("Check Text"):
        if not check_text:
            st.warning("Please enter some text to check.")
        else:
            with st.spinner("Analyzing text..."):
                time.sleep(2)
                word_count = len(check_text.split())
                avg_word_length = sum(len(word) for word in check_text.split()) / word_count if word_count > 0 else 0
                sentence_count = len(sent_tokenize(check_text))
                avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
                punctuation_count = len(re.findall(r'[.,;:!?]', check_text))
                words = check_text.lower().split()
                repeated_phrases = 0
                for i in range(len(words) - 3):
                    phrase = ' '.join(words[i:i+3])
                    if ' '.join(words[i+3:]).count(phrase) > 0:
                        repeated_phrases += 1
                humanness_score = 0
                sent_lengths = [len(s.split()) for s in sent_tokenize(check_text)]
                if sent_lengths:
                    avg_sentence_length = sum(sent_lengths) / len(sent_lengths)
                    sentence_length_variance = sum((x - avg_sentence_length) ** 2 for x in sent_lengths) / len(sent_lengths)
                    if sentence_length_variance > 10:
                        humanness_score += 20
                    elif sentence_length_variance > 5:
                        humanness_score += 10
                contractions = len(re.findall(r"\b\w+'[a-z]+\b", check_text))
                if contractions > 0:
                    humanness_score += min(15, contractions * 3)
                transitions = len(re.findall(r'\b(however|nevertheless|therefore|thus|consequently|furthermore|moreover|in addition|in fact|actually|basically|arguably|indeed|instead|meanwhile|nonetheless|otherwise|likewise|similarly|in other words|for example|for instance|in particular|specifically|especially|notably|chiefly|mainly|mostly)\b', check_text.lower()))
                humanness_score += min(15, transitions * 3)
                fillers = len(re.findall(r'\b(um|uh|like|you know|sort of|kind of|literally|basically|actually|anyway|so|well|right|okay|just)\b', check_text.lower()))
                humanness_score += min(10, fillers * 2)
                if sentence_count > 5 and abs(max(sent_lengths) - min(sent_lengths)) < 3:
                    humanness_score -= 20
                if repeated_phrases > 3:
                    humanness_score -= min(20, repeated_phrases * 2)
                humanness_score = max(0, min(100, humanness_score + 50))
                
                st.subheader("Detection Analysis Results")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown(f"""
                    <div style="text-align:center">
                        <h3>Human-likeness Score</h3>
                        <div style="margin:20px auto; width:200px; height:200px; position:relative;">
                            <div style="position:absolute; width:200px; height:200px; border-radius:50%; background:conic-gradient(from 0deg, {'green' if humanness_score > 70 else 'orange' if humanness_score > 40 else 'red'} 0%, {'green' if humanness_score > 70 else 'orange' if humanness_score > 40 else 'red'} {humanness_score}%, #e0e0e0 {humanness_score}%, #e0e0e0 100%);"></div>
                            <div style="position:absolute; width:150px; height:150px; border-radius:50%; background:white; top:25px; left:25px; display:flex; align-items:center; justify-content:center;">
                                <span style="font-size:40px; font-weight:bold; color:black;">{humanness_score}%</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.subheader("Text Metrics")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Word Count", word_count)
                    st.metric("Average Word Length", f"{avg_word_length:.2f} characters")
                    st.metric("Sentence Count", sentence_count)
                with col2:
                    st.metric("Average Sentence Length", f"{avg_sentence_length:.2f} words")
                    st.metric("Punctuation Count", punctuation_count)
                    st.metric("Repeated Phrases", repeated_phrases)
                
                st.subheader("Detection Risk")
                if humanness_score > 70:
                    st.success("✅ LOW RISK: This text has a good chance of passing AI detection tools.")
                elif humanness_score > 40:
                    st.warning("⚠️ MODERATE RISK: This text may trigger some AI detection tools. Consider further humanization.")
                else:
                    st.error("❌ HIGH RISK: This text is likely to be flagged by AI detection tools. Significant humanization recommended.")
                
                st.markdown("### Improvement Suggestions")
                suggestions = []
                if avg_sentence_length > 20:
                    suggestions.append("• Try using shorter sentences in some places")
                if avg_sentence_length < 10:
                    suggestions.append("• Try using longer, more complex sentences occasionally")
                if contractions < 3 and word_count > 200:
                    suggestions.append("• Add more contractions (e.g., don't, can't, it's)")
                if fillers < 2 and word_count > 200:
                    suggestions.append("• Add a few natural filler words (like, actually, just)")
                if transitions < 3 and word_count > 200:
                    suggestions.append("• Add more transitional phrases (however, additionally, etc.)")
                if repeated_phrases > 3:
                    suggestions.append("• Reduce repetitive phrases and patterns")
                if not suggestions:
                    suggestions.append("• Text appears natural, no specific improvements needed")
                for suggestion in suggestions:
                    st.markdown(suggestion)

with tab3:
    st.markdown("""
    ## About AI Text Humanizer
    
    This tool uses a locally running phi3 model to transform AI-generated text into highly natural, human-like writing.
    It applies advanced humanization techniques including:
    
    - Restructuring sentences with varied structures
    - Incorporating conversational fillers and transitions
    - Introducing natural redundancies and minor imperfections
    - Balancing formal and informal language usage
    
    ### How it works
    
    1. Your AI-generated text is sent to a locally running phi3 model.
    2. The model rewrites the text using advanced humanization prompts.
    3. Additional post-processing techniques further refine the natural flow.
    4. The output maintains the original meaning but reads with genuine human expression.
    
    ### Privacy & Security
    
    All processing occurs locally on your machine. No data is sent to external servers.
    
    ### Requirements
    
    - Python 3.7+
    - A locally running instance of phi3 via Ollama
    - NLTK library
    - Streamlit
    """)

if __name__ == "__main__":
    st.markdown("---")
    st.markdown("Made with ❤️ by an AI enthusiast | Not for unethical use")
