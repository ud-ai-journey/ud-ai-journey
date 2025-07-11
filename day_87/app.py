import os
from fastapi import FastAPI
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
from google.auth.transport.requests import Request
import time
import threading
import google.generativeai as genai
from google.generativeai.generative_models import GenerativeModel
import re

load_dotenv()
print("GOOGLE_API_KEY:", os.getenv("GOOGLE_API_KEY"))

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

app = FastAPI()

MODEL_NAME = "gemini-2.5-pro"  # Using Gemini 2.5 Pro model

REPLY_PROMPT = (
    "You are a polite assistant. Summarize the following email and suggest a helpful, professional reply. "
    "If the email is too long or contains images, ignore those parts and focus on the main message. "
    "If you cannot find a clear question, reply with a polite greeting.\n\nEmail: {email_body}\n\nReply:"
)

@app.on_event("startup")
def startup_event():
    """Authenticate with Gmail API on startup."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    app.state.creds = creds
    app.state.gmail_service = build('gmail', 'v1', credentials=creds)

@app.get("/")
def root():
    return {"message": "Email Auto-Reply Assistant is running!"}

def get_unread_emails(service):
    """Fetch unread emails from the user's Gmail inbox."""
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
    messages = results.get('messages', [])
    return messages

def get_email_body(service, msg_id):
    """Extract the plain text body from an email message."""
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    parts = msg['payload'].get('parts', [])
    for part in parts:
        if part['mimeType'] == 'text/plain':
            import base64
            body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
            return body
    # Fallback: try snippet
    return msg.get('snippet', '')

def mark_as_read(service, msg_id):
    service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()

def send_reply(service, msg_id, to, subject, reply_text):
    import base64
    from email.mime.text import MIMEText
    message = MIMEText(reply_text, _charset="utf-8")
    message['to'] = to
    message['subject'] = f"Re: {subject}"
    message['from'] = "Auto-Reply Assistant <pinguday111@gmail.com>"
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    # Fetch the original message to get the correct threadId
    msg = service.users().messages().get(userId='me', id=msg_id, format='metadata').execute()
    thread_id = msg.get('threadId')
    body = {'raw': raw}
    if thread_id:
        body['threadId'] = thread_id
    service.users().messages().send(userId='me', body=body).execute()

def generate_reply(email_body):
    # Remove lines starting with 'View image:' or 'Caption:'
    filtered_lines = []
    for line in email_body.splitlines():
        if not (line.strip().startswith('View image:') or line.strip().startswith('Caption:')):
            filtered_lines.append(line)
    filtered_body = '\n'.join(filtered_lines)
    # Truncate email body if too long
    max_length = 500
    if len(filtered_body) > max_length:
        filtered_body = filtered_body[:max_length] + "\n\n[Email truncated]"
    prompt = REPLY_PROMPT.format(email_body=filtered_body)
    print("Prompt sent to Gemini:", prompt)
    model = GenerativeModel(MODEL_NAME)
    response = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": 128,
            "temperature": 0.7,
        }
    )
    print("Gemini response object:", response)
    # Robustly extract the reply from the response
    try:
        candidates = getattr(response, "candidates", None)
        if candidates and hasattr(candidates[0], "content") and hasattr(candidates[0].content, "parts"):
            parts = candidates[0].content.parts
            if parts and hasattr(parts[0], "text"):
                return parts[0].text.strip()
        return "Sorry, I could not generate a reply for this email."
    except Exception as e:
        print("Error extracting Gemini reply:", e)
        return "Sorry, I could not generate a reply for this email."

def process_emails():
    service = app.state.gmail_service
    while True:
        try:
            messages = get_unread_emails(service)
            for msg in messages:
                msg_id = msg['id']
                email_body = get_email_body(service, msg_id)
                # Get email metadata
                msg_data = service.users().messages().get(userId='me', id=msg_id, format='metadata', metadataHeaders=['From', 'Subject']).execute()
                headers = {h['name']: h['value'] for h in msg_data['payload']['headers']}
                sender = headers.get('From', '')
                # Extract just the email address
                match = re.search(r'<(.+?)>', sender)
                if match:
                    to = match.group(1)
                else:
                    to = sender.strip()
                subject = headers.get('Subject', 'No Subject')
                # Generate reply
                reply_text = generate_reply(email_body)
                # Send reply
                send_reply(service, msg_id, to, subject, reply_text)
                # Mark as read
                mark_as_read(service, msg_id)
        except Exception as e:
            print(f"Error processing emails: {e}")
        time.sleep(60)  # Check every 60 seconds

@app.on_event("startup")
def start_background_email_processor():
    threading.Thread(target=process_emails, daemon=True).start()

# TODO: Add endpoint or background task to check for new emails and use Gemini for reply 