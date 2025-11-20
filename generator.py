import google.generativeai as genai
import re

class DesignGenerator:
    def __init__(self):
        self.html_wrapper = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script src="https://cdn.tailwindcss.com"></script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
                body {{ font-family: 'Inter', sans-serif; background-color: #f3f4f6; }}
                ::-webkit-scrollbar {{ display: none; }}
            </style>
        </head>
        <body class="min-h-screen flex items-center justify-center p-4 bg-gray-100">
            {content}
        </body>
        </html>
        """

    def generate_code(self, prompt, api_key):
        if not api_key:
            return self._get_error_html("Missing API Key", "Please enter your Gemini API Key in the sidebar."), "Error"

        try:
            genai.configure(api_key=api_key)
            
            # UPDATED: Prioritized models based on your specific error log
            model_candidates = [
                'gemini-2.5-flash',       # Newest available to you
                'gemini-2.0-flash',       # Robust stable option
                'gemini-2.0-flash-exp',   
                'gemini-1.5-flash',       # Fallback
                'gemini-pro'              # Fallback
            ]
            
            response = None
            last_error = None
            used_model = "Unknown"

            system_instruction = f"""
            You are an expert Frontend Engineer specializing in Tailwind CSS.
            Task: Create a modern, beautiful, and responsive HTML component based on this request: "{prompt}"
            Rules:
            1. Output ONLY the HTML code for the component.
            2. Do NOT write <html>, <head>, or <body> tags.
            3. Use 'https://source.unsplash.com/random/400x300' for placeholder images.
            4. Use FontAwesome classes for icons.
            5. Do not include markdown formatting (like ```html). Just raw code.
            """

            # 1. Try to generate with candidate models
            for model_name in model_candidates:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(system_instruction)
                    used_model = model_name
                    break # Success!
                except Exception as e:
                    last_error = e
                    continue

            # 2. If all candidates failed, run diagnostics
            if not response:
                available_models = self._list_available_models(api_key)
                error_msg = f"Failed to connect to AI models.\nLast Error: {str(last_error)}"
                
                if available_models:
                    error_msg += f"\n\n✅ AVAILABLE MODELS FOUND: {', '.join(available_models)}"
                    error_msg += "\n(The code tried to use these but failed. Check your API key permissions.)"
                else:
                    error_msg += "\n\n❌ NO MODELS FOUND. Your API key might be invalid, or the library is outdated."

                return self._get_error_html("Model Connection Failed", error_msg), "Error"

            clean_code = self._clean_response(response.text)
            return self.html_wrapper.format(content=clean_code), f"GenAI ({used_model})"

        except Exception as e:
            return self._get_error_html("System Error", f"Critical failure: {str(e)}"), "Error"

    def _list_available_models(self, api_key):
        """Diagnostics: Checks what models the API key can actually see."""
        try:
            genai.configure(api_key=api_key)
            available = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available.append(m.name)
            return available
        except:
            return []

    def _clean_response(self, text):
        text = re.sub(r'^```html', '', text, flags=re.MULTILINE)
        text = re.sub(r'^```', '', text, flags=re.MULTILINE)
        return text.strip()

    def _get_error_html(self, title, message):
        # Convert newlines to HTML breaks for better readability in the error card
        formatted_message = message.replace('\n', '<br>')
        return self.html_wrapper.format(content=f"""
        <div class="bg-white p-8 rounded-xl shadow-xl border-l-4 border-red-500 max-w-lg">
            <h2 class="text-2xl font-bold text-red-600 mb-4">{title}</h2>
            <div class="text-gray-700 text-sm font-mono bg-gray-50 p-4 rounded border border-gray-200 overflow-auto max-h-64">
                {formatted_message}
            </div>
            <p class="text-gray-500 text-xs mt-4">
                <strong>Fix:</strong> Run <code>python3 -m pip install --upgrade google-generativeai</code> in your terminal.
            </p>
        </div>
        """)
