from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pdfplumber
from docx import Document
from PIL import Image
import pytesseract

# Functions for Google Drive integration
def authenticate_google_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive

def download_file_from_drive(file_id):
    drive = authenticate_google_drive()
    file = drive.CreateFile({'id': file_id})
    file.GetContentFile(file['title'])
    return file['title']

# Functions for text extraction
def read_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def read_docx(file_path):
    doc = Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def read_image(file_path):
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img)
    return text

class ActionDownloadFile(Action):
    def name(self) -> Text:
        return "action_download_file"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        file_id = "your_google_drive_file_id_here"
        downloaded_file_name = download_file_from_drive(file_id)
        dispatcher.utter_message(f"File '{downloaded_file_name}' has been downloaded.")
        return []

class ActionExtractText(Action):
    def name(self) -> Text:
        return "action_extract_text"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        file_path = "path_to_downloaded_file"
        if file_path.endswith(".pdf"):
            text = read_pdf(file_path)
        elif file_path.endswith(".docx"):
            text = read_docx(file_path)
        elif file_path.endswith((".jpg", ".jpeg", ".png", ".gif")):
            text = read_image(file_path)
        else:
            text = "Unsupported file format. I can only extract text from PDFs, DOCX, and images."

        dispatcher.utter_message(f"Extracted text:\n{text}")
        return []

# Add your chatbot-related actions here

class ActionGreetUser(Action):
    def name(self) -> Text:
        return "action_greet_user"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Hello! How can I assist you today?")
        return []

class ActionTranslate(Action):
    def name(self) -> Text:
        return "action_translate"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Your translation action logic here
        # ...

        return []

# Define more chatbot-related actions as needed