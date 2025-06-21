# AI Meme Generator (Gemini + Gradio)

This project is an interactive AI-powered meme generator that allows users to create custom memes by simply providing a topic or emotion. It leverages Google's cutting-edge **Gemini AI model** to generate clever and relevant captions, and uses **Gradio** for a user-friendly web interface.

The generator intelligently selects a meme template from a local collection based on a tagging system, ensuring that the AI-generated caption fits a suitable visual.

## ✨ Features

* **AI-Powered Caption Generation:** Uses Google Gemini 2.0 Flash to create funny and relevant captions based on user input.
* **Intelligent Template Selection:** Picks a meme template from a local collection based on keywords/tags defined in a `meme_tags.json` file. Falls back to a random template if no direct match is found.
* **Customizable Meme Templates:** Easily add your own meme images (.jpg, .png) to the `meme_templates` folder and tag them in `meme_tags.json`.
* **Dynamic Text Placement:** Automatically draws and wraps captions onto the selected meme template, with adjustable font size and stroke for readability.
* **Web Interface:** A simple and intuitive web UI built with Gradio.
* **Secure API Key Handling:** Utilizes environment variables (via `.env` file) to keep your Google API key out of the codebase.

## 🚀 Getting Started

Follow these steps to set up and run the AI Meme Generator on your local machine.

### Prerequisites

* **Python 3.8+**
* **Git** (for cloning the repository)
* A **Google Gemini API Key**: You can obtain one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Installation

1.  **Clone the Repository:**
    Open your Git Bash or terminal and run:
    ```bash
    git clone [https://github.com/your-username/AI-Meme-Generator.git](https://github.com/your-username/AI-Meme-Generator.git)
    cd AI-Meme-Generator
    ```
    (Replace `your-username` with your actual GitHub username and `AI-Meme-Generator` if you named your repository differently.)

2.  **Create a Python Virtual Environment (Recommended):**
    This helps manage project dependencies.
    ```bash
    python -m venv venv
    ```
    * **On Windows:**
        ```bash
        ./venv/Scripts/activate
        ```
    * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(If you don't have a `requirements.txt` yet, create one in your project root with the following content:)*
    ```
    gradio
    Pillow
    google-generativeai
    python-dotenv
    ```

### 🔑 API Key Setup (Crucial!)

To keep your Gemini API key secure and out of version control:

1.  **Create a `.env` file:** In the root of your project directory (where `app.py` is located), create a new file named `.env`.
2.  **Add your API key to `.env`:**
    Open the `.env` file and add the following line, replacing `YOUR_ACTUAL_GEMINI_API_KEY_HERE` with your actual key:
    ```
    GEMINI_API_KEY=YOUR_ACTUAL_GEMINI_API_KEY_HERE
    ```
    **Important:** The `.env` file is already ignored by Git (via `.gitignore`), so it will not be uploaded to GitHub.

### 🖼️ Meme Templates and Tags Setup

1.  **Meme Templates:**
    * Create a folder named `meme_templates` in your project root.
    * Place your meme image files (`.jpg` or `.png`) inside this folder.

2.  **Meme Tags (Highly Recommended for Smart Selection):**
    * Create a file named `meme_tags.json` in your project root.
    * Populate this file with JSON data, linking your meme image paths (relative to the project root, using **forward slashes `/`**) to relevant keywords or tags.

    **Example `meme_tags.json` structure:**
    ```json
    {
      "meme_templates/distracted_boyfriend.jpg": ["distracted", "cheating", "attention", "girl", "boyfriend"],
      "meme_templates/drake_hotline_bling.png": ["approval", "disapproval", "yes", "no", "choice"],
      "meme_templates/confused_math_lady.jpg": ["confusion", "thinking", "math", "calculation", "overwhelmed"],
      "meme_templates/crying_jordan.jpg": ["sadness", "defeat", "losing", "crying", "disappointment"]
      // Add entries for all your meme templates
    }
    ```
    If `meme_tags.json` is missing or doesn't have entries for your templates, the generator will pick templates randomly.

### ✒️ Font Setup

1.  **Font File:**
    * Ensure an `arial.ttf` font file is present in your project root directory (the same folder as `app.py`).
    * If you want to use a different font, update the `FONT_PATH` variable in `app.py` to point to your desired `.ttf` file.

## ▶️ How to Run

After completing the setup steps, run the application from your terminal:

```bash
python app.py
