# 🌐 Neural English to Arabic Machine Translation Application

A senior-level Natural Language Processing (NLP) translation application powered by Hugging Face's `Helsinki-NLP/opus-mt-en-ar` MarianMT transformer model. Features an interactive **Streamlit Web UI** with native Right-To-Left (RTL) Arabic typography and a **CLI Terminal application** for rapid local testing.

---

## 📁 Project Structure

```
yolo-terminal-deployment/
│
├── app.py                     # Local Python CLI app (for local testing)
├── streamlit_app.py           # Streamlit Cloud application
├── requirements.txt           # Python dependencies
├── README.md                  # Documentation
├── packages.txt               # System dependencies (for Streamlit Cloud)
│
├── model/
│   ├── config.json            # Model parameters and pipeline configuration
│   └── labels.txt             # Target language specifications (en -> ar)
│
├── utils/
│   ├── translator.py          # Hugging Face MarianMT model loading & inference pipeline
│   └── visualization.py       # RTL text formatting, side-by-side cards, and text metrics
│
└── assets/
    └── demo.png               # App banner image for UI header
```

---

## 🚀 Quick Start & Installation

### 1. Prerequisites
Ensure you have **Python 3.10+** installed.

### 2. Install Dependencies
Navigate to the project directory and install the required packages:
```bash
pip install -r requirements.txt
```

---

## 💻 Usage Options

### Option A: Interactive Streamlit Web Application
Run the local Streamlit web interface:
```bash
streamlit run streamlit_app.py
```
Or with specific Python executable:
```bash
py -3.10 -m streamlit run streamlit_app.py
```
Then open `http://localhost:8501` in your browser.

**Features**:
- **Preset Sample Selector**: Choose from Tech, Business, Conversational, or Literature text prompts.
- **RTL Arabic Rendering**: Custom CSS rendering for proper Arabic right-to-left layout and typography.
- **Sidebar Beam Controls**: Adjust beam search size (`num_beams`) and maximum sequence length.
- **Text & Translation Statistics**: Word count metrics, character counts, and estimated reading times.

---

### Option B: Local Terminal CLI Application (`app.py`)

#### 1. Interactive CLI Mode:
```bash
python app.py
```

#### 2. Command-Line Arguments:
```bash
# Translate direct text string
python app.py --text "Machine learning is transforming language translation."

# Adjust beam search size
python app.py --text "Artificial intelligence." --beams 6

# Translate contents of a text file
python app.py --file path/to/english_doc.txt
```

---

## ☁️ Streamlit Cloud Deployment

To deploy this application to Streamlit Cloud:

1. Push this repository to **GitHub**.
2. Go to [share.streamlit.io](https://share.streamlit.io) and log in.
3. Click **New App**, select your GitHub repository and branch.
4. Set **Main file path** to `streamlit_app.py`.
5. Ensure `requirements.txt` and `packages.txt` are at the repository root.
6. Click **Deploy!**

---

## 🧠 Model Architecture & Details

- **Base Model**: `Helsinki-NLP/opus-mt-en-ar` (MarianMT Seq2Seq Transformer)
- **Tokenization**: SentencePiece Subword BPE Tokenizer
- **Decoding Algorithm**: Beam Search Decoding (configurable 1-10 beams)
- **Hardware Acceleration**: Automatic GPU (`cuda`) detection with fallback to CPU.
