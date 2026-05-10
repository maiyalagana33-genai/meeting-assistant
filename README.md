1. User types a message → index.html
The browser collects the message from the input field and fires a fetch('/chat', { method: 'POST' }) call with the text as JSON.

2. main.py receives the request
FastAPI's POST /chat route picks it up, validates the body using Pydantic (ChatRequest), and calls assistant.chat(message).

3. agent.py — the brain
MeetingAssistant.chat() does two things: first it calls self.ingester.search(query) to pull relevant meeting chunks from the database, then it builds a prompt that stitches together your system instructions + those chunks + the user's question.

4. ingestion.py + ChromaDB — the memory
MeetingIngester holds a HuggingFace embedding model and a Chroma vector store. When you search(), it converts the query to a vector and finds the 3 most similar chunks from past meetings stored on disk.

5. Gemini API — the answer
The assembled prompt is sent to gemini-2.5-flash. The API key comes from your .env file. The model's reply comes back as response.text.

6. Response flows back
agent.py returns the text → main.py wraps it in {"response": "..."} → the browser renders it as a chat bubble.
Separate ingest path: When you POST /meetings, main.py calls ingester.ingest_meeting(), which splits the transcript into 500-character chunks, embeds each one, and saves them to ChromaDB — so future searches can find them.
