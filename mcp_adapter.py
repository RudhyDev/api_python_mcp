
import requests

BASE_URL = "https://web-production-d3940.up.railway.app"

def list_tickets():
    """Lists all GLPI tickets."""
    response = requests.get(f"{BASE_URL}/tickets")
    return response.json()

def create_ticket(title: str, content: str):
    """Creates a new ticket in GLPI."""
    response = requests.post(f"{BASE_URL}/tickets", json={"title": title, "content": content})
    return response.json()

def get_ticket(ticket_id: int):
    """Retrieves a specific ticket by its ID."""
    response = requests.get(f"{BASE_URL}/tickets/{ticket_id}")
    return response.json()

def update_ticket(ticket_id: int, title: str, content: str):
    """Updates an existing ticket."""
    response = requests.put(f"{BASE_URL}/tickets/{ticket_id}", json={"title": title, "content": content})
    return response.json()

def delete_ticket(ticket_id: int):
    """Deletes a ticket from GLPI."""
    response = requests.delete(f"{BASE_URL}/tickets/{ticket_id}")
    return response.json()

def get_project_progress(tag: str):
    """Calculates the progress of a project based on its related tickets."""
    response = requests.get(f"{BASE_URL}/projects/{tag}/progress")
    return response.json()
