import random

class DesignGenerator:
    def __init__(self):
        self.base_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script src="https://cdn.tailwindcss.com"></script>
            <style>
                body {{ font-family: 'Inter', sans-serif; background-color: #f3f4f6; }}
                /* Center content vertically if needed, or allow scroll */
                .main-wrapper {{ min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }}
            </style>
        </head>
        <body>
            <div class="main-wrapper">
                {content}
            </div>
        </body>
        </html>
        """

    def get_color(self, text):
        text = text.lower()
        colors = ["red", "green", "blue", "purple", "orange", "pink", "yellow", "teal", "indigo", "gray"]
        for c in colors:
            if c in text:
                return c
        return "indigo" # Default

    def generate_code(self, prompt):
        prompt = prompt.lower()
        color = self.get_color(prompt)
        
        content = ""
        component_type = "Unknown"

        if any(x in prompt for x in ["login", "sign in", "signup", "register"]):
            component_type = "Login Screen"
            content = f"""
            <div class="bg-white p-8 rounded-xl shadow-lg w-full max-w-md border border-gray-200">
                <div class="text-center mb-6">
                    <div class="h-12 w-12 bg-{color}-600 rounded-full mx-auto flex items-center justify-center text-white font-bold text-xl">VS</div>
                    <h2 class="text-2xl font-bold text-gray-800 mt-4">Welcome Back</h2>
                    <p class="text-gray-500 text-sm">Sign in to continue</p>
                </div>
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
                        <input type="email" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-{color}-500 focus:outline-none" placeholder="user@example.com">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
                        <input type="password" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-{color}-500 focus:outline-none" placeholder="••••••••">
                    </div>
                    <button class="w-full bg-{color}-600 hover:bg-{color}-700 text-white font-bold py-2 px-4 rounded-lg transition duration-200">
                        Sign In
                    </button>
                </div>
            </div>
            """
        
        elif any(x in prompt for x in ["dashboard", "analytics", "stats"]):
            component_type = "Dashboard"
            content = f"""
            <div class="bg-white p-6 rounded-xl shadow-lg w-full max-w-4xl border border-gray-200">
                <div class="flex justify-between items-center mb-6 border-b pb-4">
                    <h1 class="text-2xl font-bold text-gray-800">Analytics Overview</h1>
                    <span class="bg-{color}-100 text-{color}-800 text-xs font-semibold px-2.5 py-0.5 rounded">Live Data</span>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div class="p-4 bg-{color}-50 rounded-lg border border-{color}-100">
                        <p class="text-gray-500 text-sm">Total Users</p>
                        <p class="text-2xl font-bold text-{color}-700">12,450</p>
                    </div>
                    <div class="p-4 bg-white rounded-lg border border-gray-200">
                        <p class="text-gray-500 text-sm">Revenue</p>
                        <p class="text-2xl font-bold text-gray-800">$45,200</p>
                    </div>
                    <div class="p-4 bg-white rounded-lg border border-gray-200">
                        <p class="text-gray-500 text-sm">Bounce Rate</p>
                        <p class="text-2xl font-bold text-gray-800">24%</p>
                    </div>
                </div>
                <div class="h-48 bg-gray-50 rounded-lg flex items-center justify-center border-2 border-dashed border-gray-300 text-gray-400">
                    [Chart Visualization Area - {color} Theme]
                </div>
            </div>
            """

        elif any(x in prompt for x in ["profile", "user", "card"]):
            component_type = "Profile Card"
            content = f"""
            <div class="bg-white rounded-2xl shadow-xl overflow-hidden w-80 border border-gray-100">
                <div class="h-32 bg-gradient-to-r from-{color}-500 to-{color}-700"></div>
                <div class="relative px-6 pb-6">
                    <div class="h-24 w-24 bg-white rounded-full p-1 absolute -top-12 border-4 border-white shadow-sm">
                        <div class="w-full h-full rounded-full bg-gray-200 flex items-center justify-center text-2xl">👤</div>
                    </div>
                    <div class="pt-14">
                        <h2 class="text-2xl font-bold text-gray-800">User Name</h2>
                        <p class="text-gray-500 text-sm">UI Designer</p>
                        <div class="mt-4 flex gap-2">
                            <button class="flex-1 bg-{color}-600 text-white py-2 rounded-full font-medium text-sm shadow-md hover:bg-{color}-700">Follow</button>
                            <button class="flex-1 bg-white border border-gray-300 text-gray-700 py-2 rounded-full font-medium text-sm hover:bg-gray-50">Message</button>
                        </div>
                    </div>
                </div>
            </div>
            """
        
        else:
            component_type = "Generic Layout"
            content = f"""
            <div class="text-center max-w-lg">
                <h1 class="text-4xl font-bold text-{color}-600 mb-4">Generated Design</h1>
                <div class="mt-8 p-6 bg-white shadow-md rounded-lg border-l-4 border-{color}-500 text-left">
                    <p class="font-semibold text-lg">Request: "{prompt}"</p>
                    <p class="mt-2 text-gray-600">We generated a generic layout because we detected a color ("{color}") but no specific component type.</p>
                    <p class="mt-4 text-sm text-gray-400">Try asking for "Login", "Dashboard", or "Profile".</p>
                </div>
            </div>
            """

        return self.base_html.format(content=content), component_type