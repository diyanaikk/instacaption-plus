import gradio as gr
import requests
import json
import re

# --- Updated Options ---
moods = ["None", "Happy", "Sad", "Romantic", "Adventurous", "Silly", "Excited", "Relaxed", "Reflective", "Grateful", "Nostalgic"]
occasions = [
    "None", "Birthday", "Vacation", "Festival", "Casual", "Throwback", "Wedding", "Date Night", "Dinner Party",
    "Sleepover", "Graduation", "Anniversary", "New Year", "Holiday", "Concert", "Road Trip"
]
styles = ["None", "Witty", "Poetic", "Minimal", "Storytelling", "Quirky", "Sassy"]
tones = ["None", "Light", "Deep", "Humorous", "Serious", "Chill", "Dramatic"]
relations = ["None", "Friends", "Family", "Partner", "Colleagues", "Pet"]

# --- Prompt Generator ---
def generate_prompt(mood, occasion, style, tone, relation):
    parts = [
        f"Write a {style.lower()} Instagram caption" if style != "None" else "Write an Instagram caption",
        f"with a {tone.lower()} tone" if tone != "None" else "",
        f"for a {mood.lower()} mood" if mood != "None" else "",
        f"for a {occasion.lower()}" if occasion != "None" else "",
        f"featuring {relation.lower()}" if relation != "None" else ""
    ]
    return ". ".join([p for p in parts if p]) + " Also generate 5 related hashtags."

# --- Hashtag Extractor (Only from end of response) ---
def extract_hashtags_from_response(response_text):
    # Look for lines with hashtags at the end
    lines = response_text.strip().split("\n")
    hashtags = []
    caption = []
    for line in lines:
        if "#" in line and len(line.strip().split()) < 10:
            hashtags.extend(re.findall(r"#\w+", line))
        else:
            caption.append(line)
    return "\n".join(caption).strip(), " ".join(sorted(set(hashtags)))

# --- Caption Generator ---
def generate_caption(mood, occasion, style, tone, relation):
    try:
        prompt = generate_prompt(mood, occasion, style, tone, relation)
        response = requests.post(
            "http://localhost:11434/api/generate",
            headers={"Content-Type": "application/json"},
            json={"model": "gemma:2b", "prompt": prompt, "stream": True},
            stream=True
        )

        full_response = ""
        for line in response.iter_lines():
            if line:
                parsed = json.loads(line.decode("utf-8"))
                full_response += parsed.get("response", "")

        caption, hashtags = extract_hashtags_from_response(full_response)
        return caption, hashtags or "No hashtags found."

    except Exception as e:
        return f"⚠️ Error: {str(e)}", "⚠️ Hashtag generation failed."

# --- JS Clipboard Functions ---
copy_caption_js = "() => { const t = document.querySelectorAll('textarea')[0]; navigator.clipboard.writeText(t.value).then(() => alert('Copied Caption ✅')); }"
copy_hashtag_js = "() => { const t = document.querySelectorAll('textarea')[1]; navigator.clipboard.writeText(t.value).then(() => alert('Copied Hashtags ✅')); }"

# --- Gradio Interface ---
with gr.Blocks(theme=gr.themes.Soft(primary_hue="violet", secondary_hue="indigo")) as demo:
    gr.Markdown("# ✨ InstaCaption+ — Caption & Hashtag Generator")

    with gr.Row():
        with gr.Column():
            mood = gr.Dropdown(moods, label="Mood", value="None")
            occasion = gr.Dropdown(occasions, label="Occasion", value="None")
            relation = gr.Dropdown(relations, label="Relation Type", value="None")
            style = gr.Dropdown(styles, label="Caption Style", value="None")
            tone = gr.Dropdown(tones, label="Tone", value="None")
            generate_btn = gr.Button("🚀 Generate")

        with gr.Column():
            caption_output = gr.Textbox(label="Generated Caption", lines=4)
            copy_caption = gr.Button("📋 Copy Caption")
            hashtag_output = gr.Textbox(label="Suggested Hashtags", lines=2)
            copy_hashtags = gr.Button("📋 Copy Hashtags")

    generate_btn.click(
        fn=generate_caption,
        inputs=[mood, occasion, style, tone, relation],
        outputs=[caption_output, hashtag_output]
    )
    copy_caption.click(None, [], [], js=copy_caption_js)
    copy_hashtags.click(None, [], [], js=copy_hashtag_js)

if __name__ == "__main__":
    demo.launch()