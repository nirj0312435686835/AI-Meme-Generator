import gradio as gr
from PIL import Image, ImageDraw, ImageFont
import google.generativeai as genai
import os
import random
from google.api_core import exceptions
import json
from dotenv import load_dotenv


load_dotenv() 
# === CONFIGURATION ===
# IMPORTANT: Replace "YOUR_ACTUAL_GEMINI_API_KEY_HERE" with your real API key
# Get your API key from Google AI Studio: https://aistudio.google.com/

api_key = os.environ.get("GEMINI_API_KEY") 
print(api_key)
genai.configure(api_key=api_key)




TEMPLATES_PATH = "./meme_templates"
OUTPUT_PATH = "./generated_memes"
FONT_PATH = "arial.ttf"

os.makedirs(OUTPUT_PATH, exist_ok=True)

MEME_TAGS_FILE = "meme_tags.json"
meme_template_data = {}
template_list = []

try:
    with open(MEME_TAGS_FILE, 'r') as f:
        loaded_tags = json.load(f)
    
    for full_path_in_json, tags in loaded_tags.items():
        filename = os.path.basename(full_path_in_json)
        expected_disk_path = os.path.join(TEMPLATES_PATH, filename)
        
        if os.path.exists(expected_disk_path):
            meme_template_data[full_path_in_json] = tags
            template_list.append(filename)
        else:
            print(f"Warning: Template '{full_path_in_json}' from '{MEME_TAGS_FILE}' not found at '{expected_disk_path}'. Skipping.")
            
    if not meme_template_data:
        print(f"Warning: No valid meme templates found with tags in '{MEME_TAGS_FILE}' or templates are missing.")
        template_list = [f for f in os.listdir(TEMPLATES_PATH) if f.endswith((".jpg", ".png"))]
    else:
        print(f"Loaded {len(meme_template_data)} meme tags for {len(template_list)} existing templates.")

except FileNotFoundError:
    print(f"Error: '{MEME_TAGS_FILE}' not found. Meme selection will be random from existing templates.")
    template_list = [f for f in os.listdir(TEMPLATES_PATH) if f.endswith((".jpg", ".png"))]
except json.JSONDecodeError:
    print(f"Error: Could not decode '{MEME_TAGS_FILE}'. Please check JSON format. Meme selection will be random.")
    template_list = [f for f in os.listdir(TEMPLATES_PATH) if f.endswith((".jpg", ".png"))]


try:
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    print("Successfully initialized Gemini model: gemini-2.0-flash")
except Exception as e:
    print(f"Error initializing Gemini model: {e}")
    print("Please ensure your API key is correct and the model 'gemini-2.0-flash' is available for your key.")
    print("You might need to update your 'google-generativeai' library: pip install --upgrade google-generativeai")
    model = None

def generate_caption(prompt):
    if model is None:
        return "Error: AI model not initialized. Please check your API key and model availability."
    try:
        response = model.generate_content(
            f"Generate only a funny and clever meme caption about: '{prompt}'. Do not include any introductory or concluding remarks, just the caption text itself. Ensure the caption is suitable for a visual meme."
        )
        caption_text = response.text.strip()
        
        lower_caption = caption_text.lower()
        prefixes_to_remove = [
            "meme caption:", "caption:", "here's a caption:", "here's your meme caption:",
            "a funny caption:", "your caption:", "meme text:", "caption text:", "here is a caption:"
        ]
        for prefix in prefixes_to_remove:
            if lower_caption.startswith(prefix):
                caption_text = caption_text[len(prefix):].strip()
                break
        
        if caption_text.startswith('"') and caption_text.endswith('"'):
            caption_text = caption_text[1:-1].strip()
        elif caption_text.startswith("'") and caption_text.endswith("'"):
            caption_text = caption_text[1:-1].strip()

        return caption_text

    except exceptions.NotFound as e:
        return f"Error: Gemini model not found or accessible. Check your API key and model name. Details: {e}"
    except exceptions.PermissionDenied as e:
        return f"Error: Permission denied. Your API key might be invalid or lack permissions. Details: {e}"
    except exceptions.ResourceExhausted as e:
        return f"Error: API rate limit exceeded or quota exhausted. Try again later. Details: {e}"
    except Exception as e:
        return f"An unexpected error occurred during caption generation: {e}"

def draw_meme(template_file, caption):
    image_path = os.path.join(TEMPLATES_PATH, template_file)
    try:
        img = Image.open(image_path).convert("RGB")
    except FileNotFoundError:
        print(f"Error: Template file not found at {image_path}. Please check TEMPLATES_PATH and template_list.")
        return None

    draw = ImageDraw.Draw(img)
    
    try:
        desired_font_size = int(img.width / 12)
        font = ImageFont.truetype(FONT_PATH, size=max(25, desired_font_size))
    except IOError:
        print(f"Warning: Font file '{FONT_PATH}' not found. Using default font. Please ensure 'arial.ttf' is accessible.")
        font = ImageFont.load_default()
    except Exception as e:
        print(f"An unexpected error occurred with font loading: {e}. Using default font.")
        font = ImageFont.load_default()

    width, height = img.size

    text_color = "white"
    stroke_color = "black"
    stroke_width = 2

    def text_wrap(text, font, max_width):
        lines = []
        if not text: return lines
        words = text.split()
        current_line = []
        for word in words:
            test_line = " ".join(current_line + [word])
            text_bbox = draw.textbbox((0,0), test_line, font=font)
            line_width = text_bbox[2] - text_bbox[0]

            if line_width <= max_width:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))
        return lines

    max_text_width = width * 0.9 
    wrapped_caption_lines = text_wrap(caption, font, max_text_width)

    total_text_height = sum(draw.textbbox((0,0), line, font=font)[3] - draw.textbbox((0,0), line, font=font)[1] for line in wrapped_caption_lines)

    y_text_start = height - total_text_height - 30 
    
    if y_text_start < 0:
        y_text_start = 10

    for line in wrapped_caption_lines:
        text_bbox = draw.textbbox((0,0), line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (width - text_width) / 2
        
        draw.text(
            (x, y_text_start), 
            line, 
            font=font, 
            fill=text_color, 
            stroke_width=stroke_width, 
            stroke_fill=stroke_color
        )
        y_text_start += text_height

    output_filename = f"meme_{random.randint(10000,99999)}.png"
    output_path = os.path.join(OUTPUT_PATH, output_filename)
    img.save(output_path)
    return output_path

def select_matching_template(topic):
    topic_lower = topic.lower()
    matching_templates = []

    for full_template_path, tags in meme_template_data.items():
        if any(topic_lower in tag.lower() for tag in tags):
            matching_templates.append(os.path.basename(full_template_path))
    
    if matching_templates:
        selected_filename = random.choice(matching_templates)
        print(f"Selected template '{selected_filename}' for topic '{topic}' based on tags.")
        return selected_filename
    else:
        print(f"No direct tag match found for '{topic}'. Selecting a random template from all available.")
        if template_list:
            return random.choice(template_list)
        else:
            return None

def generate_meme(topic):
    if not topic.strip():
        return None, "Please enter a short topic or emotion to generate a meme."
    
    if not template_list:
        return None, "No meme templates found. Please place some .jpg or .png files in the 'meme_templates' folder and ensure 'meme_tags.json' is correctly configured."

    selected_template_filename = select_matching_template(topic)
    
    if selected_template_filename is None:
        return None, "No meme templates available to generate from. Check 'meme_templates' folder and 'meme_tags.json'."

    caption = generate_caption(topic)
    
    if "Error:" in caption:
        return None, caption

    final_image_path = draw_meme(selected_template_filename, caption)
    
    if final_image_path is None:
        return None, "Failed to draw the meme. Check template files and font path."

    return final_image_path, "Meme generated successfully! (Template selected by matching your topic.)"

# --- Gradio Interface ---
iface = gr.Interface(
    fn=generate_meme,
    inputs=gr.Textbox(lines=1, placeholder="Enter a short topic or emotion (e.g., 'confusion', 'success', 'dilemma')..."),
    outputs=[gr.Image(type="filepath", label="Generated Meme"), gr.Label()],
    title="AI Meme Generator (Gemini + Tag Matching)",
    description="Enter a short topic or emotion, and this tool will pick a matching meme image and add a relevant caption using Google's Gemini AI."
)

if __name__ == '__main__':
    print("\n--- AI Meme Generator Setup ---")
    print("1. Get your Gemini API key from Google AI Studio: https://aistudio.google.com/")
    print("2. REPLACE 'YOUR_ACTUAL_GEMINI_API_KEY_HERE' in app.py with your real API key.")
    print("3. Ensure you have meme templates (.jpg or .png) in the './meme_templates' folder.")
    print("4. **CRITICAL:** Create a 'meme_tags.json' file in the same directory as 'app.py'.")
    print("   The structure should be: {'meme_templates/filename.jpg': ['tag1', 'tag2'], ...}")
    print("   Make sure the paths in 'meme_tags.json' exactly match your file paths.")
    print("   If 'meme_tags.json' is not found or templates are not tagged, meme selection will be random.")
    print("5. Make sure 'arial.ttf' (or your chosen font) is in the same directory as app.py, or update FONT_PATH.")
    print("-------------------------------\n")
    
    iface.launch()