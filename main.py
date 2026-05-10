from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from pydantic import BaseModel

from agent import MeetingAssistant

app = FastAPI(title="Meeting Assistant API")

assistant = MeetingAssistant()

# Base directory
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# ---------------- REQUEST MODELS ----------------
class ChatRequest(BaseModel):
    message: str


class MeetingUpload(BaseModel):
    title: str
    date: str
    participants: list[str]
    content: str


# ---------------- UI ROUTE ----------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    template_path = BASE_DIR / "templates" / "index.html"
    print("Template exists:", template_path.exists())

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# ---------------- CHAT API ----------------
@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        response = assistant.chat(req.message)

        return {"response": response}

    except Exception as e:
        import traceback
        print("\n===== CHAT ERROR =====")
        traceback.print_exc()
        print("======================\n")

        raise HTTPException(status_code=500, detail=str(e))


# ---------------- MEETING INGEST ----------------
@app.post("/meetings")
async def upload_meeting(meeting: MeetingUpload):
    try:
        metadata = {
            "title": meeting.title,
            "date": meeting.date,
            "participants": ", ".join(meeting.participants)
        }

        assistant.ingester.ingest_meeting(
            meeting.content,
            metadata
        )

        return {"status": "Meeting indexed successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- RESET CHAT ----------------
@app.post("/reset")
async def reset_conversation():
    assistant.conversation_history = []
    return {"status": "Conversation reset"}