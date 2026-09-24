import html

def calculate_text_metrics(english_text: str, arabic_text: str) -> dict:
    """
    Computes text statistics for source and translated text.
    """
    en_words = len(english_text.split()) if english_text else 0
    ar_words = len(arabic_text.split()) if arabic_text else 0
    en_chars = len(english_text) if english_text else 0
    ar_chars = len(arabic_text) if arabic_text else 0
    
    # Average reading speed: 200 words per minute
    reading_time_sec = round((en_words / 200) * 60, 1)
    
    return {
        "en_word_count": en_words,
        "ar_word_count": ar_words,
        "en_char_count": en_chars,
        "ar_char_count": ar_chars,
        "reading_time_sec": reading_time_sec
    }


def render_arabic_text_html(arabic_text: str, font_size: str = "1.3rem") -> str:
    """
    Renders Arabic text in proper Right-to-Left (RTL) format with custom typography.
    """
    if not arabic_text:
        return ""
    
    escaped_text = html.escape(arabic_text).replace("\n", "<br>")
    
    html_code = f"""
    <div style="
        direction: rtl;
        text-align: right;
        font-family: 'Amiri', 'Cairo', 'Segoe UI', Tahoma, Arial, sans-serif;
        font-size: {font_size};
        line-height: 1.8;
        color: #0F172A;
        background-color: #F8FAFC;
        border-right: 5px solid #0EA5E9;
        padding: 1.2rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        margin: 1rem 0;
    ">
        {escaped_text}
    </div>
    """
    return html_code


def render_side_by_side_comparison(english_text: str, arabic_text: str) -> str:
    """
    Generates HTML card displaying English source and Arabic translation side-by-side.
    """
    escaped_en = html.escape(english_text).replace("\n", "<br>")
    escaped_ar = html.escape(arabic_text).replace("\n", "<br>")
    
    html_code = f"""
    <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 1rem;">
        <div style="flex: 1; min-width: 280px; background: #1E293B; color: #F8FAFC; padding: 1.2rem; border-radius: 10px;">
            <div style="font-size: 0.85rem; text-transform: uppercase; color: #94A3B8; font-weight: 700; margin-bottom: 0.5rem;">
                🇬🇧 English Source
            </div>
            <div style="font-size: 1.05rem; line-height: 1.6;">
                {escaped_en}
            </div>
        </div>
        <div style="flex: 1; min-width: 280px; background: #0F172A; color: #F8FAFC; padding: 1.2rem; border-radius: 10px; direction: rtl; text-align: right; border-right: 4px solid #38BDF8;">
            <div style="font-size: 0.85rem; text-transform: uppercase; color: #38BDF8; font-weight: 700; margin-bottom: 0.5rem; direction: ltr; text-align: left;">
                🇸🇦 Arabic Translation (الترجمة العربية)
            </div>
            <div style="font-size: 1.25rem; line-height: 1.8; font-family: 'Amiri', 'Segoe UI', Tahoma, sans-serif;">
                {escaped_ar}
            </div>
        </div>
    </div>
    """
    return html_code


def format_cli_banner(title: str = "NLP English -> Arabic Machine Translator") -> str:
    """Formats terminal banner for app.py CLI interface."""
    border = "=" * 65
    return f"\n{border}\n  {title}\n{border}\n"
