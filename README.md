# ✨ InstaCaption+ — Caption & Hashtag Generator

InstaCaption+ is a **Python + Gradio** web app that generates creative Instagram captions and relevant hashtags based on your chosen mood, occasion, style, tone, and relation type.  
It uses the **Ollama** local LLM API with the `gemma:2b` model for fast, offline generation.

---

## 🚀 Features
- 🎯 Generate **context-aware captions**
- 🔖 Get **5 relevant hashtags**
- 🖱 One-click **copy to clipboard**
- 🎨 Simple & modern **Gradio UI**
- 🖥 Works **offline** with local LLM

---

## 🖼 Screenshot
![InstaCaption+ Screenshot](assets/screenshot.png)

> The screenshot above shows the web interface with generated captions and hashtags.

---

## 📦 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/instacaption-plus.git
cd instacaption-plus

2️⃣ Install Python dependencies
pip install -r requirements.txt

3️⃣ Install & Setup Ollama
Download from: https://ollama.ai/download

Install Ollama (it will also add it to your PATH).

Pull the required model:
"ollama pull gemma:2b"

▶ Usage
Start the app
"python app.py"
- Open the local URL shown in the terminal (e.g., http://127.0.0.1:7860).
- Select options → Click Generate → Copy your caption & hashtags.

🧪 Testing Ollama API
Before running the main app, you can test your Ollama API connection:
"python test_ollama.py"

👤 Author
Diya J Naik
GitHub: diyanaikk

