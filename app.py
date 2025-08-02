import gradio as gr
from transformers import pipeline
from langdetect import detect
from gtts import gTTS
import os
import json

# Load translation model
pipe = pipeline("translation", model="facebook/nllb-200-distilled-600M", device="cpu")

# Load language mappings
with open("language_codes.json", "r", encoding="utf-8") as f:
    language_list = json.load(f)
    language_dict = {entry["Language"]: entry["FLORES-200 code"] for entry in language_list}

# ISO → FLORES mapping (for langdetect)
iso_to_flores_map = {
    'en': 'eng_Latn', 'hi': 'hin_Deva', 'fr': 'fra_Latn', 'de': 'deu_Latn',
    'es': 'spa_Latn', 'ta': 'tam_Taml', 'te': 'tel_Telu', 'gu': 'guj_Gujr',
    'bn': 'ben_Beng', 'pa': 'pan_Guru', 'ur': 'urd_Arab', 'zh-cn': 'zho_Hans'
}

# FLORES → ISO for gTTS
flores_to_iso_tts = {
    'eng_Latn': 'en', 'hin_Deva': 'hi', 'fra_Latn': 'fr', 'deu_Latn': 'de',
    'spa_Latn': 'es', 'tam_Taml': 'ta', 'tel_Telu': 'te', 'guj_Gujr': 'gu',
    'ben_Beng': 'bn', 'pan_Guru': 'pa', 'urd_Arab': 'ur', 'zho_Hans': 'zh-CN'
}

def get_flores_code(lang_name):
    return language_dict.get(lang_name.strip(), "eng_Latn")

def detect_flores_from_text(text):
    try:
        iso_code = detect(text)
        return iso_to_flores_map.get(iso_code, "eng_Latn"), iso_code
    except:
        return "eng_Latn", "en"

def translate_and_speak(text, source_lang, target_lang):
    try:
        if source_lang == "Auto-Detect":
            source_code, iso = detect_flores_from_text(text)
            source_lang_display = f"Auto-detected ({iso})"
        else:
            source_code = get_flores_code(source_lang)
            source_lang_display = source_lang

        target_code = get_flores_code(target_lang)

        result = pipe(text, src_lang=source_code, tgt_lang=target_code)
        translated_text = result[0]['translation_text']

        tts_lang = flores_to_iso_tts.get(target_code, "en")
        tts = gTTS(translated_text, lang=tts_lang)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)

        display_text = f"🔤 From: {source_lang_display}\n🎯 To: {target_lang}\n\n📝 Translated Text:\n{translated_text}"
        return display_text, audio_bytes
    except Exception as e:
        return f"❌ Error: {str(e)}", None

# 🔁 Swap source ↔ target
def swap_langs(src, tgt):
    if tgt == "Auto-Detect":
        tgt = "English"
    if src == "Auto-Detect":
        src = "English"
    return gr.update(value=tgt), gr.update(value=src)

# UI language dropdowns
language_options = ["Auto-Detect"] + list(language_dict.keys())

# 🌐 UI Design
with gr.Blocks(css="styles.css") as iface:
    gr.Markdown(
        """
        <div style="text-align: center;">
        <h1 style="color: #4A90E2;">🌐 GenAI Multilingual Translator</h1>
        <p style="font-size: 16px; color: gray;">Translate text between 200+ languages with voice support</p>
        </div>
        """
    )

    with gr.Row():
        input_text = gr.Textbox(label="Enter Text", placeholder="Type your sentence here...", lines=4)

    with gr.Row():
        source_lang = gr.Dropdown(label="Source Language", choices=language_options, value="Auto-Detect")
        swap_btn = gr.Button("🔁 Swap")
        target_lang = gr.Dropdown(label="Target Language", choices=list(language_dict.keys()), value="Hindi")

    with gr.Row():
        translate_btn = gr.Button("🚀 Translate", scale=2)

    with gr.Row():
        output_text = gr.Textbox(label="Translation Result", lines=6, interactive=False)
        audio_output = gr.Audio(label="Text-to-Speech")

    translate_btn.click(
        fn=translate_and_speak,
        inputs=[input_text, source_lang, target_lang],
        outputs=[output_text, audio_output]
    )

    swap_btn.click(
        fn=swap_langs,
        inputs=[source_lang, target_lang],
        outputs=[source_lang, target_lang]
    )

iface.launch()
