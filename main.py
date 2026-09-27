import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
import webbrowser
import datetime

# Background styling (Dark Theme)
Window.clearcolor = (0.08, 0.09, 0.12, 1)

class MustaraAssistantApp(App):
    def build(self):
        self.title = "Mustara AI Assistant"
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header / Title Bar
        header = Label(
            text="★ MUSTARA AI ASSISTANT ★",
            font_size='22sp',
            bold=True,
            size_hint=(1, 0.08),
            color=(0.2, 0.8, 1, 1)
        )
        main_layout.add_widget(header)
        
        # Chat Display Area
        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.chat_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=8,
            padding=[5, 5]
        )
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.scroll_view.add_widget(self.chat_layout)
        main_layout.add_widget(self.scroll_view)
        
        # Initial Welcome Message
        self.add_message("Mustara: नमस्ते! मैं आपका Mustara Assistant हूँ। आप मुझसे समय, तारीख, मौसम, YouTube या Google सर्च पूछ सकते हैं।", is_user=False)
        
        # Bottom Input Area
        input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.12), spacing=8)
        
        self.user_input = TextInput(
            hint_text="यहाँ टाइप करें...",
            multiline=False,
            font_size='16sp',
            background_color=(0.15, 0.16, 0.22, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.2, 0.8, 1, 1),
            size_hint=(0.75, 1)
        )
        self.user_input.bind(on_text_validate=self.process_command)
        input_layout.add_widget(self.user_input)
        
        send_btn = Button(
            text="भेजें",
            bold=True,
            font_size='16sp',
            background_color=(0.1, 0.6, 0.9, 1),
            size_hint=(0.25, 1)
        )
        send_btn.bind(on_press=self.process_command)
        input_layout.add_widget(send_btn)
        
        main_layout.add_widget(input_layout)
        return main_layout

    def add_message(self, text, is_user=True):
        msg_color = (0.2, 0.8, 1, 1) if is_user else (1, 1, 1, 1)
        msg_label = Label(
            text=text,
            font_size='15sp',
            size_hint_y=None,
            color=msg_color,
            text_size=(Window.width * 0.9, None),
            halign='left',
            valign='middle'
        )
        msg_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1] + 15))
        self.chat_layout.add_widget(msg_label)
        
        # Auto-scroll to bottom
        Clock.schedule_once(lambda dt: setattr(self.scroll_view, 'scroll_y', 0), 0.1)

    def process_command(self, instance):
        query = self.user_input.text.strip()
        if not query:
            return
        
        self.add_message(f"आप: {query}", is_user=True)
        self.user_input.text = ""
        
        q_lower = query.lower()
        
        if "time" in q_lower or "समय" in q_lower:
            now = datetime.datetime.now().strftime("%I:%M %p")
            reply = f"Mustara: अभी का समय है: {now}"
            
        elif "date" in q_lower or "तारीख" in q_lower or "दिनांक" in q_lower:
            today = datetime.datetime.now().strftime("%d %B %Y")
            reply = f"Mustara: आज की तारीख है: {today}"
            
        elif "youtube" in q_lower:
            search_query = query.replace("youtube", "").replace("खोजो", "").strip()
            if search_query:
                url = f"https://www.youtube.com/results?search_query={search_query}"
                reply = f"Mustara: YouTube पर '{search_query}' सर्च कर रहा हूँ..."
            else:
                url = "https://www.youtube.com"
                reply = "Mustara: YouTube खोल रहा हूँ..."
            webbrowser.open(url)
            
        elif "google" in q_lower or "search" in q_lower:
            search_query = query.replace("google", "").replace("search", "").replace("खोजो", "").strip()
            url = f"https://www.google.com/search?q={search_query}"
            reply = f"Mustara: Google पर '{search_query}' खोज रहा हूँ..."
            webbrowser.open(url)
            
        elif "whatsapp" in q_lower or "व्हाट्सएप" in q_lower:
            url = "https://api.whatsapp.com"
            reply = "Mustara: WhatsApp ओपन कर रहा हूँ..."
            webbrowser.open(url)
            
        elif "weather" in q_lower or "मौसम" in q_lower:
            url = "https://www.google.com/search?q=weather+today"
            reply = "Mustara: आज के मौसम की जानकारी खोल रहा हूँ..."
            webbrowser.open(url)
            
        elif "hello" in q_lower or "hi" in q_lower or "नमस्ते" in q_lower:
            reply = "Mustara: हैलो! बताइए, मैं आज आपकी क्या सहायता कर सकता हूँ?"
            
        elif "who are you" in q_lower or "तुम कौन हो" in q_lower:
            reply = "Mustara: मैं Mustara AI Assistant हूँ, आपका निजी मोबाइल साथी!"
            
        else:
            url = f"https://www.google.com/search?q={query}"
            reply = f"Mustara: मुझे इसके बारे में सटीक उत्तर नहीं मिला, Google पर सर्च किया जा रहा है..."
            webbrowser.open(url)
            
        self.add_message(reply, is_user=False)

if __name__ == '__main__':
    MustaraAssistantApp().run()
