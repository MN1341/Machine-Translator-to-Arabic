import os
import streamlit as st
from PIL import Image
from utils.translator import EnglishToArabicTranslator
from utils.visualization import (
    render_arabic_text_html,
    render_side_by_side_comparison,
    calculate_text_metrics
)

# 1. Page Configuration
st.set_page_config(
    page_title="AI English to Arabic NLP Translator",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for Styling & RTL Arabic Rendering
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;600;700&display=swap');
    
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .stTextArea textarea {
        font-size: 1.05rem;
        border-radius: 10px;
        border: 1px solid #CBD5E1;
    }
    .metric-box {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .metric-num {
        font-size: 1.6rem;
        font-weight: 700;
        color: #38BDF8;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

# 3. Cache Model Loader
@st.cache_resource
def get_translator():
    config_path = os.path.join(os.path.dirname(__file__), "model", "config.json")
    translator = EnglishToArabicTranslator(config_path=config_path)
    translator.load_model()
    return translator

# Initialize translator instance
translator = get_translator()

# 4. Banner Header Image
banner_path = os.path.join(os.path.dirname(__file__), "assets", "demo.png")
if os.path.exists(banner_path):
    banner_img = Image.open(banner_path)
    st.image(banner_img, use_container_width=True)

st.markdown("<div class='main-title'>🌐 Neural English → Arabic Machine Translator</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>State-of-the-Art MarianMT Sequence-to-Sequence NLP Engine (Helsinki-NLP)</div>", unsafe_allow_html=True)

# 5. Sidebar Controls & Model Metadata
st.sidebar.header("⚙️ Translation Parameters")

num_beams = st.sidebar.slider(
    "Beam Search Size (num_beams):",
    min_value=1,
    max_value=10,
    value=4,
    help="Higher values improve translation quality but take slightly longer."
)

max_token_length = st.sidebar.slider(
    "Max Token Length:",
    min_value=64,
    max_value=1024,
    value=512,
    step=64,
    help="Maximum token sequence length allowed for sequence generation."
)

st.sidebar.markdown("---")
st.sidebar.header("ℹ️ Model Specifications")
st.sidebar.info("""
- **Model**: `Helsinki-NLP/opus-mt-en-ar`
- **Architecture**: MarianMT Seq2Seq Transformer
- **Target Language**: Arabic (Right-To-Left RTL)
- **Framework**: PyTorch + Hugging Face Transformers
""")

labels_path = os.path.join(os.path.dirname(__file__), "model", "labels.txt")
if os.path.exists(labels_path):
    with st.sidebar.expander("📋 View Model Metadata"):
        with open(labels_path, "r", encoding="utf-8") as f:
            st.text(f.read())

# 6. Sample Presets & Text Input
st.subheader("1. Enter English Text")

preset_options = {
    "Custom Text": "",
    "Artificial Intelligence (Tech)": "Artificial intelligence and machine learning are transforming how humans process and understand natural language across the globe.",
    "Business & Finance": "Our quarterly financial reports indicate significant revenue growth across all international subsidiary branches.",
    "Conversational Greetings": "Good morning! Welcome to our AI platform. How can I assist you with your translation project today?",
    "Literature & Philosophy": "Knowledge is a light that illuminates the mind and expands human understanding."
}

selected_preset = st.selectbox(
    "Choose a Sample Input Preset (Optional):",
    options=list(preset_options.keys()),
    index=0
)

default_text = preset_options[selected_preset]

user_input = st.text_area(
    "Source English Text:",
    value=default_text,
    height=140,
    placeholder="Type or paste English text here..."
)

# 7. Translation Action Button & Output
col_btn, col_clear = st.columns([1, 4])
with col_btn:
    translate_clicked = st.button("✨ Translate to Arabic", type="primary", use_container_width=True)

if translate_clicked or (user_input and selected_preset != "Custom Text"):
    if not user_input.strip():
        st.warning("Please enter some English text to translate.")
    else:
        with st.spinner("Translating text with MarianMT transformer model..."):
            arabic_result = translator.translate(
                text=user_input,
                max_length=max_token_length,
                num_beams=num_beams
            )
            
        metrics = calculate_text_metrics(user_input, arabic_result)
        
        st.markdown("---")
        st.subheader("2. Arabic Translation Output (الترجمة العربية)")
        
        # Tabs for Output Views
        tab_formatted, tab_side_by_side, tab_raw = st.tabs(["✨ Formatted RTL Card", "📖 Side-by-Side Comparison", "📄 Raw Text"])
        
        with tab_formatted:
            st.markdown(render_arabic_text_html(arabic_result, font_size="1.4rem"), unsafe_allow_html=True)
            st.download_button(
                label="📥 Download Arabic Text (.txt)",
                data=arabic_result,
                file_name="arabic_translation.txt",
                mime="text/plain"
            )

        with tab_side_by_side:
            st.markdown(render_side_by_side_comparison(user_input, arabic_result), unsafe_allow_html=True)

        with tab_raw:
            st.text_area("Arabic Text (Raw Output):", value=arabic_result, height=120)

        # Text Metrics Bar
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("3. Text & Translation Statistics")
        
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        
        with m_col1:
            st.markdown(f"""
            <div class='metric-box'>
                <div class='metric-num'>{metrics['en_word_count']}</div>
                <div class='metric-label'>English Words</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col2:
            st.markdown(f"""
            <div class='metric-box'>
                <div class='metric-num'>{metrics['ar_word_count']}</div>
                <div class='metric-label'>Arabic Words</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col3:
            st.markdown(f"""
            <div class='metric-box'>
                <div class='metric-num'>{metrics['en_char_count']} / {metrics['ar_char_count']}</div>
                <div class='metric-label'>EN / AR Characters</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col4:
            st.markdown(f"""
            <div class='metric-box'>
                <div class='metric-num'>~{metrics['reading_time_sec']}s</div>
                <div class='metric-label'>Est. Reading Time</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Powered by Hugging Face MarianMT • Helsinki-NLP/opus-mt-en-ar • Streamlit NLP App")
