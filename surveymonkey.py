import json
import sys
import requests

# Replace with your actual SurveyMonkey API access token
ACCESS_TOKEN = ""
API_URL = "https://api.surveymonkey.com/v3"
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

def create_survey(survey_data):
    """Creates a survey on SurveyMonkey based on the provided JSON data."""
    if not survey_data or "Survey_Name" not in survey_data:
        print("Error: Invalid survey data format. 'Survey_Name' key missing.")
        return None

    survey_title = "My Automated Survey"
    pages_data = survey_data["Survey_Name"]
    elements = []

    for page_title, questions in pages_data.items():
        page_elements = []
        for question_name, details in questions.items():
            answers = details.get("Answers", [])
            if not answers:
                print(f"Warning: Question '{question_name}' has no answers. Skipping.")
                continue

            question = {
                "type": "single",
                "family": "single_choice",
                "subtype": "vertical",
                "answers": {
                    "choices": [{"text": ans} for ans in answers]
                },
                "heading": details.get("Description", question_name),
                "required": False,
            }
            page_elements.append({"question": question})

        if page_elements:
            elements.append({"title": page_title, "questions": page_elements})

    survey_payload = {
        "title": survey_title,
        "pages": elements,
    }

    try:
        response = requests.post(f"{API_URL}/surveys", headers=HEADERS, json=survey_payload)
        response.raise_for_status()
        survey_info = response.json()
        print(f"Survey '{survey_title}' created successfully. Survey ID: {survey_info['id']}")
        return survey_info['id']
    except requests.exceptions.RequestException as e:
        print(f"Error creating survey: {e}")
        return None

def read_email_list(file_path):
    """Reads email addresses from a text file."""
    try:
        with open(file_path, 'r') as f:
            emails = [line.strip() for line in f if line.strip()]
        return emails
    except FileNotFoundError:
        print(f"Error: Email list file not found at '{file_path}'")
        return []

def create_collector(survey_id):
    """Creates a collector for the survey."""
    if not survey_id:
        return None

    collector_payload = {
        "name": "Email Collector",
        "type": "email",
    }

    try:
        response = requests.post(f"{API_URL}/surveys/{survey_id}/collectors", headers=HEADERS, json=collector_payload)
        response.raise_for_status()
        collector_info = response.json()
        print(f"Collector created successfully. Collector ID: {collector_info['id']}")
        return collector_info['id']
    except requests.exceptions.RequestException as e:
        print(f"Error creating collector: {e}")
        return None

def send_invitations(collector_id, email_list):
    """Sends survey invitations to the provided email addresses."""
    if not collector_id or not email_list:
        print("Error: Collector ID or email list is empty.")
        return

    recipients = [{"email": email} for email in email_list]
    invitation_payload = {"recipients": recipients}

    try:
        response = requests.post(f"{API_URL}/collectors/{collector_id}/messages", headers=HEADERS, json=invitation_payload)
        response.raise_for_status()
        invitation_info = response.json()
        print(f"Invitations sent successfully. Invitation IDs: {[inv['id'] for inv in invitation_info.get('data', [])]}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending invitations: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_survey_invite.py <survey_questions.json> <recipient_emails.txt>")
        sys.exit(1)

    questions_file = sys.argv[1]
    emails_file = sys.argv[2]

    try:
        with open(questions_file, 'r') as f:
            survey_data = json.load(f)
        print("Survey data loaded successfully.")
    except FileNotFoundError:
        print(f"Error: Questions file not found at '{questions_file}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{questions_file}'")
        sys.exit(1)

    email_list = read_email_list(emails_file)
    if len(email_list) < 2:
        print("Error: Please provide at least 2 recipient email addresses.")
        sys.exit(1)

    # Count total questions
    question_count = 0
    for page_questions in survey_data.get("Survey_Name", {}).values():
        question_count += len(page_questions)

    if question_count < 3:
        print(f"Error: The survey must contain at least 3 questions. Found {question_count}.")
        sys.exit(1)

    survey_id = create_survey(survey_data)
    if survey_id:
        collector_id = create_collector(survey_id)
        if collector_id:
            send_invitations(collector_id, email_list)
