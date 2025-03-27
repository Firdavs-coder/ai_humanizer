# AI Text Humanizer Documentation

## Overview 🤖→🧠
AI Text Humanizer is a Streamlit-based web application that transforms AI-generated text into more natural, human-like writing using the phi3 language model and advanced text processing techniques.

## Installation 🚀

```sh
# Install required dependencies
pip install -r requirements.txt

# Start Ollama with phi3 model
ollama run phi3

# Launch the application
streamlit run ai_humanizer.py
```

## Features ✨

### Text Humanization
- Advanced text transformation using phi3 model
- Adjustable temperature control (0.1-1.0)
- Multiple humanization techniques:
  - Smart typo insertion
  - Natural punctuation variation
  - Organic repetition
  - Dynamic text formatting

### AI Detection Analysis
- Real-time detection risk assessment
- Human-likeness scoring
- Comprehensive text metrics
- Actionable improvement suggestions

## Usage Guide 📖

1. **Text Humanization**
   - Open the Text Humanizer tab
   - Input your AI-generated text
   - Adjust settings in sidebar
   - Click "Humanize Text"

2. **Detection Check**
   - Navigate to AI Detection Check tab
   - Paste text for analysis
   - Review detailed metrics and scores
   - Follow improvement suggestions

## Components 🔧

### Core Engine
- phi3 model integration via Ollama API
- Advanced post-processing pipeline
- Real-time text analysis
- Metric calculation system

### User Interface
- Three-tab layout:
  - Text Humanizer
  - AI Detection Check
  - About
- Interactive controls
- Real-time progress tracking
- Detailed statistics display

## Technical Requirements 💻

- Python 3.7+
- Ollama with phi3 model
- NLTK library
- Streamlit
- Internet connection for initial setup

## Privacy & Security 🔒

- Local processing only
- No external API calls
- Data remains on your machine
- Open-source codebase

## Best Practices 💡

1. Start with default settings
2. Adjust temperature for desired variation
3. Enable techniques selectively
4. Use detection check for validation
5. Iterate based on feedback

## Limitations ⚠️

- Requires local Ollama setup
- Performance depends on hardware
- Results vary with input length
- Heuristic-based detection

## Legal Note ⚖️

This tool is intended for legitimate use cases only. Not for unethical purposes.

## Contributing 🤝

Pull requests are welcome. For major changes, please open an issue first to discuss proposed changes.

---

Made with ❤️ by an AI enthusiast