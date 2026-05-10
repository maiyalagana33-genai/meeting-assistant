import os

from dotenv import load_dotenv
import google.generativeai as genai

from ingestion import MeetingIngester

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)


class MeetingAssistant:

    def __init__(self):

        self.ingester = MeetingIngester()
        self.conversation_history = [] 
        self.system_prompt = """
        You are a meeting assistant.

        Help users:
        - Recall meetings
        - Summarize discussions
        - Generate action items
        """

    def chat(self, user_message: str):

        try:
            relevant_docs = self.ingester.search(user_message)
        except Exception:
            relevant_docs = []

        context = "\n\n".join(
            [doc.page_content for doc in relevant_docs]
        )

        prompt = f"""
        {self.system_prompt}

        Meeting Context:
        {context}

        User Question:
        {user_message}
        """

        response = model.generate_content(prompt)

        return response.text