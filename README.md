# 🌍 GenAI Multilingual Translator

An AI-powered multilingual translator that supports over **200 languages** with **auto language detection** and **text-to-speech (TTS)** output. Built using Python, Gradio, and Hugging Face Transformers, and deployed on Hugging Face Spaces.

## 🚀 Live Demo

👉 [Click here to try it on Hugging Face Spaces](https://huggingface.co/spaces/Srion123/genai-translator)

---

## 🔑 Features

- 🌐 Translate between **200+ languages**
- 🧠 **Auto-detect** source language
- 🗣️ **Text-to-Speech (TTS)** for translated output
- 📦 Simple and interactive **Gradio UI**
- 💬 Powered by **facebook/nllb-200-distilled-600M** model from Hugging Face

---

## 🛠️ Tech Stack

- Python 🐍
- Gradio
- Hugging Face Transformers
- NLLB-200 Model (`facebook/nllb-200-distilled-600M`)
- langdetect (for auto language detection)
- gTTS (Google Text-to-Speech)
- Hugging Face Spaces (for free deployment)

---

## ⚙️ How It Works

1. User inputs text.
2. Language is auto-detected using `langdetect`.
3. Translation is performed using the **NLLB-200 model**.
4. Translated text is passed through **gTTS** to generate audio.
5. Final output includes translated text and a play button for audio.

---

## 📦 Installation (for local run)

```bash
git clone https://huggingface.co/spaces/Srion123/genai-translator
cd genai-translator
pip install -r requirements.txt
python app.py
```

---

##📁 Folder Structure

genai-translator/
├── app.py
├── requirements.txt
├── static/
│   └── output.mp3
└── README.md

---

##🧪 Model Used

-facebook/nllb-200-distilled-600M
A multilingual machine translation model by Meta AI that supports 200+ languages.

---

##👩‍💻 Author

Srishti
B.Tech CSE Student 
📍 Prayagraj, India
